from __future__ import unicode_literals
import logging
import shlex
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from subprocess import check_call
from os import environ

log = logging.getLogger(__name__)

def download_url(url, temp_directory='/tmp'):
    user = environ['SPOTIFY_USER']
    passwd = environ['SPOTIFY_PASS']
    cmd = ".venv/bin/spotify-ripper -k spotify_appkey.key -d {} -u {} -p {}" \
          " -A -f  {}  ".format(temp_directory, user, passwd, url)
    # I hate this...
    check_call(shlex.split(cmd))
    scrub_filenames(temp_directory)
    embed_metadata(temp_directory, url)
    return temp_directory


def scrub_filenames(temp_directory):
    for f in temp_directory.files():
        f.rename(f.replace(' ', '_'))

def embed_metadata(filepath, url):
    for mp3 in filepath.files('*.mp3'):
        audiofile = MP3(mp3, ID3=EasyID3)
        audiofile.tags['website'] = url
        audiofile.tags.save()
        print "Updated audio file with {}".format(audiofile.tags)
