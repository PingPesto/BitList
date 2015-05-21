#!/usr/bin/env python

# Redis Connection agent/manager - because having redis littered around my
# code was OBNOXIOUS

from os import environ
from redis import Redis


# Redis DB schema
# 0 / Job Data
# 1 / Song Data
# 2 / MUSIC DB Cache - 15 minute cache
# 5 / Cache Data - 1 hour cache



class Cache:

    def __init__(self):
        redis_dsn = environ['REDIS_HOST']
        self.redis_host = redis_dsn.split(':')[0]
        self.redis_port = redis_dsn.split(':')[1]

    def connection(self, database=0):
        return Redis(host=self.redis_host, port=self.redis_port, db=database)



