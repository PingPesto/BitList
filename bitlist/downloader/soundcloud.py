from __future__ import unicode_literals
import logging
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import shlex
from subprocess import check_call

log = logging.getLogger(__name__)

def download_url(url, temp_directory='/tmp'):
    cmd = ".venv/bin/youtube-dl {} --add-metadata --format=mp3 " \
          "-o {}/%(title)s.%(ext)s".format(url, temp_directory)
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
