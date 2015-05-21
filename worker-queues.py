import os
import urlparse
from redis import Redis
from rq import Worker, Queue, Connection
import sys

listen = [sys.argv[1]]

redis_url = os.getenv('REDIS_URL')
if not redis_url:
    raise RuntimeError('Setup Redis first.')

urlparse.uses_netloc.append('redis')
url = urlparse.urlparse(redis_url)
conn = Redis(host=url.hostname, port=url.port, db=0, password=url.password)

with Connection(conn):
    worker = Worker(map(Queue, listen))
    worker.work()
