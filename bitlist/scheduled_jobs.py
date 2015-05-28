from bitlist.models.playlist import Playlist
from bitlist.player import client as mpd
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

#TODO: Make this modular depending on active context of playlist
def playlist_watcher():
   p = Playlist.get('default')
   p.sync_with_mpd(mpd())


scheduler = BackgroundScheduler()
scheduler.add_job(playlist_watcher, 'interval',  minutes=.5, id='playlist_watcher')
scheduler.start()


