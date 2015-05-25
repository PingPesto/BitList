from .user import User
import datetime
from pyramid_mongoengine import MongoEngine
import random

db = MongoEngine()

class Song(db.Document):

    title = db.StringField(required=True)
    url = db.StringField(required=True)
    artist= db.StringField()
    original_url = db.StringField()
    album = db.StringField()
    album_art = db.StringField()
    addedby = db.ReferenceField(User, reverse_delete_rule=db.NULLIFY)
    rand = db.FloatField(unique=True)
    tags = db.ListField()
    created_on = db.DateTimeField(default=datetime.datetime.now)
    updated_on = db.DateTimeField(default=datetime.datetime.now)

    @classmethod
    def get_by_id(cls, id):
        song = cls.objects.get_or_404(id=id)
        return song

    @classmethod
    def get_by_url(cls, url):
        song = cls.objects.get_or_404(url=url)
        return song

    @classmethod
    def get_random(cls):
        random.seed()
        rand = random.random()

        songs = cls.objects(rand__gte=rand).limit(1)
        return songs.first()

    def clean(self):
        if not self.rand:
            self.rand = generate_random()

def generate_random():
    random.seed()
    return random.random()
