#!/usr/bin/env python

# Transactional wrapping class to interact with an MPD Daemon. Leverages the
# smarts of MPDClient2 python library. Stubbing out a lot of the common request

from contextlib import contextmanager
import logging
from mpd import MPDClient, ConnectionError
from os import environ

log = logging.getLogger(__name__)

remote = environ['MPD_HOST']
host = remote.split(':')[0]
port = remote.split(':')[1]

client = MPDClient()
client.timeout = 10
client.idletimeout = None


@contextmanager
def daemon_transaction(request):
    ''' Allows transactional requests between MPD and our API.
        This is important as we only want to open the TCP socket when we have
        business to conduct. This will keep our API from tanking when it cannot
        communicate with MPD
    '''
    try:
        log.debug('Connecting...')
        request.connect(host, port)
        yield
    except ConnectionError as e:
        if e.message == "Already connected":
            yield
        else:
            raise
    except:
        raise
    finally:
        request.close()
        request.disconnect()
        log.debug('Disconnected')


def stop():
    with daemon_transaction(client):
        client.stop()

def play():
    with daemon_transaction(client):
        client.play()

def skip():
    with daemon_transaction(client):
        client.next()

def enqueue(link):
     with daemon_transaction(client):
        client.add(link)

def status():
    with daemon_transaction(client):
        return client.status()

def clear():
    with daemon_transaction(client):
        return client.clear()

def playlist():
    with daemon_transaction(client):
        return client.playlist()

