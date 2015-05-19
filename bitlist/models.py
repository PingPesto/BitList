from pyramid.security import Allow, Everyone

from sqlalchemy import (
    Column,
    Integer,
    Text,
    String,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(
    sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Song(Base):
    __tablename__ = 'songs'
    uid = Column(Integer, primary_key=True)
    title = Column(String(250))
    artist = Column(String(250))
    album = Column(String(250))
    album_art = Column(Text)
    url = Column(String(300), unique=True)
    original_url = Column(Text)
    addedby = Column(Text)

    def __init__(self, title, url, artist=None, original_url=None, album=None,
                  album_art=None, addedby=None):
        self.title = title
        self.url = url
        self.artist= artist
        self.original_url = original_url
        self.album = album
        self.album_art = album_art
        self.addedby = addedby

    def __json__(self, request):
        return dict(
            uid=self.uid,
            title=self.title,
            artist=self.artist,
            album=self.album,
            album_art=self.album_art,
            url=self.url,
            original_url=self.original_url,
            addedby=self.addedby)

# TODO: Needs a valid salting alg for storing passwords
class User(Base):
    __tablename__ = 'users'
    uid = Column(Integer, primary_key=True)
    name = Column(String(250))
    email = Column(String(250), unique=True)
    password = Column(String(250))

    def __init__(self, name, email):
        self.name = name
        self.email = email




class Root(object):
    __acl__ = [(Allow, Everyone, 'view'),
               (Allow, 'group:editors', 'edit')]

    def __init__(self, request):
        pass
