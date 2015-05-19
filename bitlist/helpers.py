#!/usr/bin/env python

from bitlist.models import DBSession, Song
import os
import random
from redis import Redis

redis_dsn = os.environ['REDIS_HOST']
redis_host = redis_dsn.split(':')[0]
redis_port = redis_dsn.split(':')[1]




def pexpand(path):
    return os.path.abspath(os.path.expanduser(path))

def output_dir(out):
    if not os.path.exists(out):
        os.makedirs(out)

def get_archive_links():
    conn = Redis(host=redis_host, port=redis_port, db=1)
    archive = conn.keys()
    links = []
    for f in archive:
        links.append(conn.get(f))

    return links

def get_random_song():
    total_songs = DBSession.query(Song).count()
    randoms = random.sample(range(total_songs),2)
    random_song = DBSession.query(Song).filter_by(uid=randoms[0]).one()
    return random_song
