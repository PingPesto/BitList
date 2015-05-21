#!/usr/bin/env python
from bitlist.models.song import Song
from bitlist.db.cache import Cache
import json
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import os
import pickle
import random
from redis import Redis
from urllib import unquote_plus

cache = Cache()

def sanitize_string(song_title):
    # do basic transforms/filters on the song_title passed
    song_title = song_title.replace('_', ' ')
    song_title = song_title.replace('.mp3', '')
    return unquote_plus(song_title)

def get_song_by_id(id):
    cache = Cache().connection(2)
    return pickle.loads(cache.get(id))

def get_random_song():
    cache = Cache().connection(2)
    #total_library_size = len(cache.keys())
    #randoms = random.sample(range(1, total_library_size),1)[0]
    random_song = pickle.loads(cache.get(cache.randomkey()))
    return random_song

def redis_song_library():
    conn = cache.connection(2)
    archive = conn.keys()
    links = []
    for f in archive:
        links.append(pickle.loads(conn.get(f)))
    return links

def add_to_playlist(request, song_id):
    song = get_song_by_id(song_id)
    playlist = cache.connection(3)
    playlist.rpush('playlist', song.id)
    request.mpd.add(song.url)
    return request.mpd.playlist()

def current_playlist():
    playdb = cache.connection(3)
    songdb = cache.connection(2)
    serialized_playlist = playdb.lrange('playlist', 0, -1)
    playlist = []
    for s in serialized_playlist:
        song = pickle.loads(songdb.get(s))
        playlist.append({ 'id': song.id, 'title': song.title})
    return playlist

def update_database(filepath, s3_url):
    audiofile = MP3(afile, ID3=EasyID3)
    s = Song(audiofile.tags['title'],
             original_url=audiofile.tags['website'])
    s.save()
    return s
