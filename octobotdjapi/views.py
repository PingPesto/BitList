from helpers import get_archive_links
from pyramid.view import view_config
import player
import jobs
import json

# ======    FRONT END ROUTES   ==========
@view_config(route_name='player', renderer='templates/player.jinja2')
def player_view(request):
    return { 'playlist': request.mpd.playlist(),
             'status': request.mpd.status(),
             'listen-url': os.environ['LISTEN_URL'] }




# =======   MUSIC DAEMON CONTROLS =======

@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project': 'octobot-dj-api'}

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

@view_config(route_name='playlistseed', renderer='json')
def player_playlist_seed(request):
    for song in get_archive_links():
        request.mpd.add(song)
    return {'Status': 'Success'}

@view_config(route_name='playlistclear', renderer='json')
def player_playlist_clear(request):
    request.mpd.clear()
    return {'Status': 'Success'}

@view_config(route_name='playlistenqueue', renderer='json')
def player_playlist_enqueue(request):
    request.mpd.add(song)
    return {'Status': 'Success'}


# ======== FETCH API CONTROLS =======

@view_config(route_name='fetch_youtube', renderer='json')
def fetch_youtube_url(request):
    pid = jobs.enqueue_transcode_youtube_link(request.matchdict['videoid'])
    return {'JobID': pid}

# ======== Redis API CONTROLS =======
@view_config(route_name='update_cache', renderer='json')
def enqueue_update_cache(request):
    jobs.enqueue_s3_scraper()
    return {'Status': 'Success'}

