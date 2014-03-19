from pyramid.httpexceptions import HTTPMovedPermanently, HTTPNotFound
from pyramid.view import view_config

from foomn.shortenkey import (
    expand_shortenkey,
    InvalidShortenKey,
    ShortenKeyDoesNotExist,
)


@view_config(route_name='top', renderer="home.mako")
def home(request):
    return {}


@view_config(route_name='expand')
def expand(request):
    shortenkey = request.matchdict['shortenkey']
    try:
        url = expand_shortenkey(shortenkey)
    except (InvalidShortenKey, ShortenKeyDoesNotExist):
        raise HTTPNotFound

    return HTTPMovedPermanently(location=url)


@view_config(route_name='api_shorten')
def api_shorten(request):
    return {}


@view_config(route_name='api_expand')
def api_expand(request):
    return {}
