from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from foomn.models import (
    Base,
    DBSession,
)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
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
