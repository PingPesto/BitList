from bitlist.models.song import Song
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from urllib import unquote_plus

#TODO move this to the song model, and implement clean()
def sanitize_string(song_title):
    # do basic transforms/filters on the song_title passed
    song_title = song_title.replace('_', ' ')
    song_title = song_title.replace('.mp3', '')
    return unquote_plus(song_title)

def update_database(filepath, s3_url):
    print s3_url
    audiofile = MP3(filepath, ID3=EasyID3)
    print audiofile.tags['title']
    print audiofile.tags['website']
    s = Song()
    s.title = title=audiofile.tags['title'][0]
    s.url = s3_url
    s.original_url = audiofile.tags['website'][0]
    s.save()
    return s
