from pyramid.events import NewRequest
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from .security import groupfinder
import player

from .models import (
    DBSession,
    Base,
    )

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings, root_factory='bitlist.models.Root')
    config.include('pyramid_chameleon')
    config.include('pyramid_jinja2')

    # Security Policies
    authn_policy = AuthTktAuthenticationPolicy(
        'sosecret', callback=groupfinder, hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('songs', '/songs')
    config.add_route('player', '/player')
    config.add_route('play', '/player/play')
    config.add_route('skip', '/player/skip')
    config.add_route('status', '/player/status')
    config.add_route('playsong', '/player/play/{song}')
    config.add_route('playlist', '/player/playlist')
    config.add_route('playlistshuffle', '/player/playlist/shuffle')
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

    # import ipdb; ipdb.set_trace();
    return config.make_wsgi_app()

