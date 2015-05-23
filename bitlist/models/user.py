import cryptacular.bcrypt
from bitlist.db.cache import Cache
from os import getenv
import pickle
from pyramid.security import Everyone
from pyramid.security import Authenticated
from pyramid.security import Allow

crypt = cryptacular.bcrypt.BCRYPTPasswordManager()


def groupfinder(userid, request):
    cache = Cache().connection(4)
    user = pickle.loads(cache.get(userid))
    return user.groups

class User():
    def __init__(self, email, password, username):
        self.username = username
        self.email = email
        self._set_password(password)
        self.groups = ['listen']

    def password(self):
        return self.__password

    def _set_password(self, password):
        self.__password = self._hash_password(password)


    @classmethod
    def get_by_email(cls, email):
        cache = Cache().connection(4)
        return pickle.loads(cache.get(email))

    @classmethod
    def check_password(cls, email, password):
        cache = Cache().connection(4)
        user = cls.get_by_email(email)
        if not user:
            return false
        return crypt.check(user.password(), password)


    def _hash_password(self, password):
        return unicode(crypt.encode(password))


    def __json__(self, request):
        return dict(
                id=self.id,
                name=self.name,
                email=self.email,
                groups=self.groups,
                )


    def save(self):
        cache = Cache().connection(4)
        cache.set(self.email, pickle.dumps(self))


class RootFactory(object):
    __acl__ = [
        (Allow, Authenticated, 'listen'),
    ]

    def __init__(self, request):
        pass  # pragma: no cover
