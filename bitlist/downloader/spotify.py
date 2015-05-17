from __future__ import unicode_literals
import logging
import shlex
from subprocess import check_call
from os import environ

log = logging.getLogger(__name__)

def download_url(url, temp_directory='/tmp'):
    user = environ['SPOTIFY_USER']
    passwd = environ['SPOTIFY_PASS']
    cmd = ".venv/bin/spotify-ripper -k spotify_appkey.key -d {} -u {} -p {}" \
          " -A -F  {}  ".format(temp_directory, user, passwd, url)
    # I hate this...
    check_call(shlex.split(cmd))

    return temp_directory


