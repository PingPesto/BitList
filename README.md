# BitList

This [pyramid](http://www.pylonsproject.org/) project is used to control the
`mpd` player running in a [Docker container](https://github.com/PingPesto/Dockerfiles/tree/master/music-server).

## Configuration

This project makes use of [Honcho](https://github.com/nickstenning/honcho) Procfiles

This means your app configuration can be stored in `.env` to appropriately share
among the processes.

    REDIS_HOST='localhost:6379'
    MPD_HOST='localhost:6600'
    S3_ACCESS_KEY='XXX'
    S3_SECRET_KEY='XXXX'
    S3_BUCKET='my-storage-bin'

## Getting Started

To get started with the app stack:

    docker run -d -p 8000:8000 -p 6600:6600 -v /path/to/music:/opt/music lazypower/mpd-server
    docker run -d -p 6379:6379 redis

Make sure you've got a git clone of the source tree

### A note about Dependencies in Python

> If you're a casual python user, you should look into venv style dependency
management. It isolates application dependencies from the HOST python install.
this is particularly useful when you're on a POSIX system, as python is often
a core dependency for smooth operation. Polluting that environment may yield
odd behavior.

[Python Virtualenv Docs](https://virtualenv.pypa.io/en/latest/)

#### To DEV
Install deps, and execute

    python setup.py develop
    honcho start

#### To Run

edit the Procfile, and change the line:

    web: pserve development.ini --reload

to

    web: pserve production.ini

then Install deps, and execute

    python setup.py install
    honcho start
