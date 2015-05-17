from bitlist.downloader import youtube
from bitlist.downloader import soundcloud
from bitlist.downloader import spotify
from boto.s3.connection import S3Connection
from os import environ, remove, rmdir
from path import Path
from player import client as mpd
from redis import Redis
from rq import Queue
from rq.decorators import job
import shutil
from tempfile import mkdtemp
import tinys3
import urllib

s3_access_key = environ['S3_ACCESS_KEY']
s3_secret_key = environ['S3_SECRET_KEY']
s3_bucket = environ['S3_BUCKET']


redis_dsn = environ['REDIS_HOST']
redis_host = redis_dsn.split(':')[0]
redis_port = redis_dsn.split(':')[1]

worker_redis_conn = Redis(host=redis_host, port=redis_port, db=0)
metadata_redis_conn = Redis(host=redis_host, port=redis_port, db=1)

# Define the RQ Redis Queue

@job('high', connection=worker_redis_conn, timeout=120)
def upload_file(filepath, delete=False, playlist_update=True):
    base = filepath.basename()
    with open(filepath, 'rb') as f:
        conn = tinys3.Connection(s3_access_key, s3_secret_key, tls=True)
        conn.upload(base, f, s3_bucket)

    if delete:
        remove(filepath)
        if len(filepath.dirname().files('*.mp3')) == 0:
            filepath.dirname().rmdir_p()

    if playlist_update and ".mp3" in filepath.basename():
        # Calculate the URL without an S3 query
        key_url = "https://s3.amazonaws.com/{}/{}".format(s3_bucket,
                   filepath.basename())
        player = mpd()
        player.add(key_url)
        print "Added {}".format(key_url)


# Transcode and upload youtube music/videos
@job('low', connection=worker_redis_conn, timeout=900)
def transcode_youtube_link(url):
    # Inspect the incoming variable to see if it is a URL or an ID
    if not "youtube.com" in url:
        url = "https://www.youtube.com/watch?v={}".format(url)
    tmp = mkdtemp()
    # if the job fails for any reason, cleanup. Re-enqueue will create
    # a new tmpdir and attempt the job again.
    try:
        youtube.download_url(url, temp_directory=tmp)
    except:
        shutil.rmtree(tmp)
        print "Exception occurred during transcoding"

    p = Path(tmp)
    for f in p.files():
        upload_file.delay(f, delete=True)

# Transcode and upload soundcloud music
@job('low', connection=worker_redis_conn, timeout=900)
def transcode_soundcloud_link(user, song):
    url = "https://www.soundcloud.com/{}/{}".format(user, song)

    tmp = mkdtemp()
    try:
        soundcloud.download_url(url, temp_directory=tmp)
    except:
        shutil.rmtree(tmp)

    p = Path(tmp)
    for f in p.files():
        upload_file.delay(f, delete=True)


# Transcode and upload spotify music
@job('low', connection=worker_redis_conn, timeout=900)
def transcode_spotify_link(url):
    tmp = mkdtemp()
    try:
        spotify.download_url(url, temp_directory=tmp)
    except:
        shutil.rmtree(tmp)

    p = Path(tmp)
    for f in p.files():
        upload_file.delay(f, delete=True)


@job('high', connection=worker_redis_conn, timeout=120)
def scan_s3_files():
    conn = S3Connection(s3_access_key, s3_secret_key)
    bucket = conn.get_bucket(s3_bucket)
    for item in bucket.list():
        if item.name == None: continue
        url = "http://s3.amazonaws.com/{}/{}".format(s3_bucket,item.name)
        url = urllib.quote(url, safe="%/:=&?~#+!$,;'@()*[]")
        redis_conn.set(item.name, url)

