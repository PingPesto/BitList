from bitlist.db.cache import Cache
import pickle
from pyramid.security import Allow, Everyone
from uuid import uuid4

class Song():
    def __init__(self, title, url, artist=None, original_url=None, album=None,
                  album_art=None, addedby=None, id=None):
        if not id:
            self.id = str(uuid4())
        self.title = title
        self.url = url
        self.artist= artist
        self.original_url = original_url
        self.album = album
        self.album_art = album_art
        self.addedby = addedby

    def __json__(self, request):
        return dict(
            id=self.id,
            title=self.title,
            artist=self.artist,
            album=self.album,
            album_art=self.album_art,
            url=self.url,
            original_url=self.original_url,
            addedby=self.addedby)

    def save(self):
        cache = Cache().connection(2)
        cache.set(self.id, pickle.dumps(self))



class Root(object):
    __acl__ = [(Allow, Everyone, 'view'),
               (Allow, 'group:editors', 'edit')]

    def __init__(self, request):
        pass
