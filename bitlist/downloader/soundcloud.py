from __future__ import unicode_literals
import logging
import shlex
from subprocess import check_call

log = logging.getLogger(__name__)

def download_url(url, temp_directory='/tmp'):
    cmd = ".venv/bin/youtube-dl {} --add-metadata --format=mp3 " \
          "-o {}/%(title)s.%(ext)s".format(url, temp_directory)
    # I hate this...
    check_call(shlex.split(cmd))
    scrub_filenames(temp_directory)
    return temp_directory

def scrub_filenames(temp_directory):
    for f in temp_directory.files():
        f.rename(f.replace(' ', '_'))
