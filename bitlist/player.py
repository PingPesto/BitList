#!/usr/bin/env python

# Transactional wrapping class to interact with an MPD Daemon. Leverages the
# smarts of MPDClient2 python library. Stubbing out a lot of the common client

from contextlib import contextmanager
import logging
from mpd import MPDClient, ConnectionError
from os import environ

log = logging.getLogger(__name__)

def client():
    remote = environ['MPD_HOST']
    host = remote.split(':')[0]
    port = remote.split(':')[1]

    client = MPDClient()
    client.timeout = 10
    client.idletimeout = None
    client.connect(host, port)
    return client

#Used in Player Connection manager Tween
@contextmanager
def connection_manager(request):
    ''' Allows transactional requests between MPD and our API.
        This is important as we only want to open the TCP socket when we have
        business to conduct. This will keep our API from tanking when it cannot
        communicate with MPD
    '''
    import ipdb; ipdb.set_trace()
    try:
        log.debug('Connecting...')
        request.mpd.connect(host, port)
        yield
    except ConnectionError as e:
        if e.message == "Already connected":
            yield
        else:
            raise
    except:
        raise
    finally:
        request.mpd.close()
        request.mpd.disconnect()
        log.debug('Disconnected')

