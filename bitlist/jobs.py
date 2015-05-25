from bitlist.db.cache import Cache
from bitlist.downloader import youtube
from bitlist.downloader import soundcloud
from bitlist.downloader import spotify
from bitlist.models.playlist import Playlist
from bitlist.models.song import Song
from boto.s3.connection import S3Connection
from helpers import sanitize_string
from helpers import update_database
from os import environ, remove
from path import Path
from player import client as mpd
from rq import Queue
from rq.decorators import job
from tempfile import mkdtemp
import tinys3
import urllib
from pyramid_mongoengine import MongoEngine
db = MongoEngine()

# TODO: This seems bad, dont hard-code the db
db.connect('bitlist')

s3_access_key = environ['S3_ACCESS_KEY']
s3_secret_key = environ['S3_SECRET_KEY']
s3_bucket = environ['S3_BUCKET']

cache = Cache()
worker_redis_conn = cache.connection(0)
metadata_redis_conn = cache.connection(1)

# Define the RQ Redis Queue

@job('high', connection=worker_redis_conn, timeout=120)
def upload_file(filepath, delete=False, playlist_update=True):
    base = filepath.basename()
    if ".info" in base:
        print "Not uploading json"
        return
    key_url = "http://s3.amazonaws.com/{}/{}".format(s3_bucket,
                   base)
    with open(filepath, 'rb') as f:
        conn = tinys3.Connection(s3_access_key, s3_secret_key, tls=True)
        conn.upload(base, f, s3_bucket)

    song = update_database(filepath, key_url)

    if delete:
        remove(filepath)
        if len(filepath.dirname().files('*.mp3')) == 0:
            filepath.dirname().rmdir_p()

    if playlist_update and ".mp3" in filepath.basename():
        player = mpd()
        p = Playlist.get('default')
        p.add(player, song.id)
        print "Added {}".format(key_url)


@job('high', connection=worker_redis_conn, timeout=120)
def warm_db_cache():
    conn = S3Connection(s3_access_key, s3_secret_key)
    bucket = conn.get_bucket(s3_bucket)
    for item in bucket.list():
        if item.name == None: continue
        if not '.mp3' in item.name: continue

        url = "http://s3.amazonaws.com/{}/{}".format(s3_bucket,item.name)
        url = urllib.quote(url, safe="%/:=&?~#+!$,;'@()*[]")
        title = sanitize_string(item.name.replace('.mp3', ''))
        s = Song(title, url)
        s.save()


# TODO: Clean these up - and turn this entire 3 method body block into a single
# DRY method to work w/ the proper queue system.

# Transcode and upload youtube music/videos
@job('youtube', connection=worker_redis_conn, timeout=900)
def transcode_youtube_link(url):
    # Inspect the incoming variable to see if it is a URL or an ID
    if not "youtube.com" in url:
        url = "https://www.youtube.com/watch?v={}".format(url)
    dtmp = mkdtemp()
    tmp = Path(tmp)
    # if the job fails for any reason, cleanup. Re-enqueue will create
    # a new tmpdir and attempt the job again.
    try:
        youtube.download_url(url, temp_directory=tmp)
    except:
        tmp.rmtree(tmp)
        print "Exception occurred during transcoding"

    p = Path(tmp)
    for f in p.files():
        upload_file.delay(f, delete=True)

# Transcode and upload soundcloud music
@job('soundcloud', connection=worker_redis_conn, timeout=900)
def transcode_soundcloud_link(user, song):
    url = "https://www.soundcloud.com/{}/{}".format(user, song)

    dtmp = mkdtemp()
    tmp = Path(dtmp)
    try:
        soundcloud.download_url(url, temp_directory=tmp)
    except:
        tmp.rmtree(tmp)

    for f in tmp.files():
        upload_file.delay(f, delete=True)


# Transcode and upload spotify music
@job('spotify', connection=worker_redis_conn, timeout=900)
def transcode_spotify_link(url):
    dtmp = mkdtemp()
    tmp = Path(dtmp)
    try:
        spotify.download_url(url, temp_directory=tmp)
    except:
        tmp.rmtree(tmp)

    for f in tmp.files():
        upload_file.delay(f, delete=True)


