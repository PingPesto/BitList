from __future__ import unicode_literals
import logging
import youtube_dl
from tempfile import mkdtemp

log = logging.getLogger(__name__)


class MyLogger(object):
    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)

def my_hook(d):
    if d['status'] == 'finished':
        print('Completed downloading {}'.format(d['filename']))
        print("Starting transcoder")



# Define YoutubeDL options
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': MyLogger(),
    'outtmpl': '/tmp/%(title)s.%(ext)s',
    'restrictfilenames': True,
    'progress_hooks': [my_hook],
}

def download_url(url, temp_directory='/tmp'):
    ydl_opts['outtmpl'] = '{}/%(title)s.%(ext)s'.format(temp_directory)
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        foo = ydl.download([url])
    return temp_directory
