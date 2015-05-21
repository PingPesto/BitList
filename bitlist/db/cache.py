#!/usr/bin/env python

# Redis Connection agent/manager - because having redis littered around my
# code was OBNOXIOUS

from os import getenv
from redis import Redis
import urlparse

# Redis DB schema
# 0 / Job Data
# 1 / Song Data
# 2 / MUSIC DB Cache
# 3 / Playlist Cache



class Cache:

    def __init__(self):
        redis_dsn = getenv('REDIS_URL')
        if not redis_dsn:
            raise RuntimeError('Setup Redis first.')

        urlparse.uses_netloc.append('redis')
        url = urlparse.urlparse(redis_dsn)
        self.host = url.hostname
        self.port = url.port
        self.password = url.password

    def connection(self, database=0):
        return Redis(host=self.host, port=self.port, db=database, password=self.password)

