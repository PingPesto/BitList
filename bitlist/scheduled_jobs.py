from bitlist.models.playlist import Playlist
from bitlist.player import client as mpd
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from os import getenv

# Disable the obnoxious scheduler when doing development thru
# ENV vars
SCHEDULE_DISABLED = getenv('BITLIST_SCHEDULE_DISABLED')

#TODO: Make this modular depending on active context of playlist
def playlist_watcher():
   p = Playlist.get('default')
   p.sync_with_mpd(mpd())


if not SCHEDULE_DISABLED:
    scheduler = BackgroundScheduler()
    scheduler.add_job(playlist_watcher, 'interval',  minutes=.5, id='playlist_watcher')
    scheduler.start()


