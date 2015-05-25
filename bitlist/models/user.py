import cryptacular.bcrypt
import datetime
from os import getenv
from pyramid_mongoengine import MongoEngine
from pyramid.security import Everyone
from pyramid.security import Authenticated
from pyramid.security import Allow

crypt = cryptacular.bcrypt.BCRYPTPasswordManager()
db = MongoEngine()

class User(db.Document):

    email = db.EmailField(required=True)
    username = db.StringField(required=True)
    password = db.StringField(required=True)
    avatar = db.URLField()
    groups = db.ListField(default=['listen'])
    created_on = db.DateTimeField(default=datetime.datetime.now)
    updated_on = db.DateTimeField(default=datetime.datetime.now)

    @classmethod
    def get_by_email(cls, email):
        user = cls.objects.get_or_404(email=email)
        return user

    @classmethod
    def check_password(cls, email, password):
        user = cls.get_by_email(email)
        if not user:
            return false
        return crypt.check(user.password, password)

    def create_password(self, password):
        self.password = hash_password(password)

    def clean(self):
        if not self.avatar:
            self.avatar = generate_avatar(self.email)

class RootFactory(object):
    __acl__ = [
        (Allow, Authenticated, 'listen'),
    ]

    def __init__(self, request):
        pass  # pragma: no cover

def groupfinder(email, request):
    user = User.objects.get_or_404(email=email)
    return user.groups


def hash_password(password):
    return unicode(crypt.encode(password))

def generate_avatar(email):
    # stubbed as paas until i decide to fold this into bitlist
    base_url = "http://robohash.org/{}.png"
    return base_url.format(email)




