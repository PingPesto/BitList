from bitlist.db.cache import Cache
from helpers import get_archive_links, get_random_song, redis_song_library
import jobs
import json
import player
from pyramid.view import view_config
from .models.song import Song


# ======    FRONT END ROUTES   ==========
@view_config(route_name='player', renderer='templates/player.jinja2')
def player_view(request):
    server_path = "http://{}:8000".format(request.host.split(':')[0])
    status = request.mpd.status()
    playlist = request.mpd.playlist()
    if status['state'] != 'play':
        random_song = get_random_song()
        request.mpd.add(random_song.url)
        request.mpd.play()
        status['state'] = 'play'
    return { 'playlist': playlist,
             'status': status,
             'player_host': server_path,
             'library': redis_song_library()}


@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project': 'bitlist'}

@view_config(route_name='songs', renderer='json')
def library(request):
    available_music = redis_song_library()
    return dict(songs=available_music)

# =======   MUSIC DAEMON CONTROLS =======
@view_config(route_name='play', renderer='json')
def player_play(request):
    request.mpd.play()
    return {'Status': 'Success'}

@view_config(route_name='skip', renderer='json')
def player_skip(request):
    request.mpd.next()

@view_config(route_name='status', renderer='json')
def player_status(request):
    return request.mpd.status()

@view_config(route_name='playlist', renderer='json')
def player_playlist(request):
    return request.mpd.playlist()

@view_config(route_name='playlistshuffle', renderer='json')
def player_playlist_shuffle(request):
    request.mpd.shuffle()
    return request.mpd.playlist()

@view_config(route_name='playlistseed', renderer='json')
def player_playlist_seed(request):
    pid = jobs.warm_db_cache.delay()
    return {'JobID': pid.id}


@view_config(route_name='playlistclear', renderer='json')
def player_playlist_clear(request):
    request.mpd.clear()
    return request.mpd.playlist()

@view_config(route_name='playlistenqueue', renderer='json')
def player_playlist_enqueue(request):
    song_id = request.matchdict['song']
    song = pickle.loads(request.song_cache.get(song_id))
    request.mpd.add(song.url)
    return request.mpd.playlist()


# ======== FETCH API CONTROLS =======

@view_config(route_name='fetch_youtube', renderer='json')
def fetch_youtube_url(request):
    pid = jobs.transcode_youtube_link.delay(request.matchdict['videoid'])
    return {'JobID': pid.id}

@view_config(route_name='fetch_soundcloud', renderer='json')
def fetch_soundcloud_url(request):
    pid = jobs.transcode_soundcloud_link.delay(request.matchdict['user'],
                                               request.matchdict['songid'])
    return {'JobID': pid.id}

@view_config(route_name='fetch_spotify', renderer='json')
def fetch_spotify_url(request):
    pid = jobs.transcode_spotify_link.delay(request.matchdict['resource'])
    return {'JobID': pid.id}



# ======== Redis API CONTROLS =======
@view_config(route_name='update_cache', renderer='json')
def enqueue_update_cache(request):
    jobs.enqueue_s3_scraper()
    return {'Status': 'Success'}

