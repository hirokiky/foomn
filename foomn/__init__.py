import os

from paste.deploy.loadwsgi import appconfig
from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from foomn.models import (
    Base,
    DBSession,
)


_settings = {}


def set_settings(sets):
    global _settings
    _settings = sets


def get_settings():
    return _settings.copy()


def init_settings():
    ini = os.environ.get(
        'PYRAMID_SETTINGS',
        os.path.abspath(os.path.join(os.path.dirname(__file__), '../development.ini'))
    )

    set_settings(appconfig('config:%s' % ini, 'settings'))


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    init_settings()
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('top', '/')
    config.add_route('expand', '/{shortenkey}')
    config.add_route('api_expand', '/api/expand/')
    config.add_route('api_shorten', '/api/shorten/')
    config.scan('.views')

    return config.make_wsgi_app()
