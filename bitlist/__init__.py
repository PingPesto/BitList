from bitlist.models.user import groupfinder
from bitlist.models.user import RootFactory
from bitlist.models.user import User
from os import getenv
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.events import NewRequest
from pyramid.config import Configurator
from pyramid.security import unauthenticated_userid
import player

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    authn_policy = AuthTktAuthenticationPolicy(getenv('AUTH_SECRET'),
            callback=groupfinder, hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config = Configurator(root_factory=RootFactory, settings=settings)
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.include('pyramid_chameleon')
    config.include('pyramid_jinja2')
    config.include('pyramid_mongoengine')
    config.add_settings({"mongodb_name": "bitlist", 'alias': 'default'})
    config.add_connection_database()

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('js', 'static/js', cache_max_age=3600)
    config.add_static_view('images', 'static/images', cache_max_age=3600)
    config.add_static_view('css', 'static/css', cache_max_age=3600)
    config.add_static_view('fonts', 'static/fonts', cache_max_age=3600)

    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('home', '/')
    config.add_route('songs', '/songs')
    config.add_route('songinfo', '/songs/{songid}')
    config.add_route('player', '/player')
    config.add_route('play', '/player/play')
    config.add_route('skip', '/player/skip')
    config.add_route('status', '/player/status')
    config.add_route('playsong', '/player/play/{song}')
    config.add_route('playlist', '/player/playlist')
    config.add_route('playlistclear', '/player/playlist/clear')
    config.add_route('playlistseed', '/player/playlist/seed')
    config.add_route('playlistenqueue', '/player/playlist/queue/{song}')
    config.add_route('fetch_youtube', '/fetch/youtube/{videoid}')
    config.add_route('fetch_soundcloud', '/fetch/soundcloud/{user}/{songid}')
    config.add_route('fetch_spotify', '/fetch/spotify/{resource}')
    config.add_route('update_cache', '/cache/update')


    config.scan()
    config.registry.mpd_client = player.client()
    config.add_request_method(lambda req : player.client(), "mpd", reify=True)
    config.add_request_method(get_user, 'user', reify=True)

    # import ipdb; ipdb.set_trace();
    return config.make_wsgi_app()


def get_user(request):
    userid = unauthenticated_userid(request)
    if userid is not None:
        return User.get_by_email(userid)

