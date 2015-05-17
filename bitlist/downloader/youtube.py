from __future__ import unicode_literals
import json
import logging
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from path import path
from tempfile import mkdtemp
import youtube_dl

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
    'writeinfojson': True,
    'outtmpl': '/tmp/%(title)s.%(ext)s',
    'restrictfilenames': True,
    'progress_hooks': [my_hook],
}

def download_url(url, temp_directory='/tmp'):
    ydl_opts['outtmpl'] = '{}/%(title)s.%(ext)s'.format(temp_directory)
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        foo = ydl.download([url])
    embed_metadata(temp_directory)
    return temp_directory



# Mutgaten EasyID3 supports a limited tagset, keeping here for reference
##['albumartistsort',
# 'lyricist', 'date', 'performer', 'tracknumber', 'album', 'mood', 'copyright',
# 'author', 'website', 'compilation', 'genre', 'discnumber', 'language',
# 'artist', 'title', 'bpm']



# Embed data received from Youtube - this is lossy and prone to error if we
# save anything other than title as the link description
def embed_metadata(filepath):
    filepath = path(filepath)
    for data in filepath.files('*.info.json'):
        with open(data) as f:
            trackdata = json.loads(f.read())
        afile = "{}.mp3".format(data.split('.info')[0])
        audiofile = MP3(afile, ID3=EasyID3)
        audiofile.tags['title'] = trackdata['title']
        audiofile.tags['website'] = trackdata['webpage_url']
        audiofile.tags.save()
        print "Updated audio file with {}".format(audiofile.tags)

def trim_silence(filepath):
    pass
    # reminder - how to find if a binary exists in path
    # distutils.spawn.find_executable('foo')
