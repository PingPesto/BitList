from boto.s3.connection import S3Connection
from tempfile import mkdtemp
from octobotdjapi.downloader import youtube
from os import environ, remove
from path import Path
from redis import Redis
from rq import Queue
from player import client as mpd
import shutil
import tinys3
import urllib
import player

s3_access_key = environ['S3_ACCESS_KEY']
s3_secret_key = environ['S3_SECRET_KEY']
s3_bucket = environ['S3_BUCKET']


redis_dsn = environ['REDIS_HOST']
redis_host = redis_dsn.split(':')[0]
redis_port = redis_dsn.split(':')[1]

# Define the RQ Redis Queue
q = Queue(connection=Redis(host=redis_host, port=redis_port, db=0))
# Define the Redis DB for metadata about our files
redis_conn = Redis(host=redis_host, port=redis_port, db=1)

# use tinys3 to upload files - its lightweight
def upload_file(filepath, delete=False, playlist_update=True):
    base = filepath.basename()
    print(filepath)
    with open(filepath, 'rb') as f:
        conn = tinys3.Connection(s3_access_key, s3_secret_key, tls=True)
        conn.upload(base, f, s3_bucket)
        if playlist_update:
            # Calculate the URL without an S3 query
            key_url = "https://s3.amazonaws.com/{}/{}".format(s3_bucket,
                       filepath.basename())
            player = mpd()
            player.add(key_url) # TODO
    if delete:
            remove(filepath)


# use boto to list files, its huge
def scan_s3_files():
    conn = S3Connection(s3_access_key, s3_secret_key)
    bucket = conn.get_bucket(s3_bucket)
    for item in bucket.list():
        if item.name == None: continue
        url = "http://s3.amazonaws.com/{}/{}".format(s3_bucket,item.name)
        url = urllib.quote(url, safe="%/:=&?~#+!$,;'@()*[]")
        redis_conn.set(item.name, url)

# =============== Queueing Functions =================
#   use these methods to actually enqueue the jobs

# Transcode and upload youtube music/videos
def enqueue_transcode_youtube_link(url):
    # Inspect the incoming variable to see if it is a URL or an ID
    if not "youtube.com" in url:
        url = "https://www.youtube.com/watch?v={}".format(url)
    tmp = mkdtemp()
    transcoder = q.enqueue(youtube.download_url, url, temp_directory=tmp)
    p = Path(tmp)
    q.enqueue(enqueue_file_upload, p, depends_on=transcoder)

# The youtube-downloader doesn't descriminate. It will process
# entire channels if you tell it to. Handle cases with multiple
# files, and singletons
def enqueue_file_upload(filepath):
    p = Path(filepath)
    if p.isdir():
        for file in p.files():
            q.enqueue(upload_file, file, delete=True)
    else:
        q.enqueue(upload_file, filepath, delete=True)

# Pulls all file paths down from S3 - useful when seeding the playlist
def enqueue_s3_scraper():
    q.enqueue(scan_s3_files)
