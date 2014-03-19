import unittest
from unittest import mock

from pyramid import testing


def _registerRoutes(config):
    config.add_route('expand', '/{shorten_key}')


class TestExpand(unittest.TestCase):
    def _callFUT(self, *args, **kwargs):
        from foomn.views import expand
        return expand(*args, **kwargs)

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test__invalid_shorten_key(self):
        request = testing.DummyRequest()
        request.matchdict['shortenkey'] = 'a'

        from foomn.shortenkey import InvalidShortenKey
        with mock.patch('foomn.views.expand_shortenkey',
                        side_effect=InvalidShortenKey, autospec=True) as m:
            from pyramid.httpexceptions import HTTPNotFound
            self.assertRaises(HTTPNotFound, self._callFUT, request)

        m.assert_called_with('a')

    def test__shortenkey_does_not_exist(self):
        request = testing.DummyRequest()
        request.matchdict['shortenkey'] = 'aa'

        from foomn.shortenkey import ShortenKeyDoesNotExist
        with mock.patch('foomn.views.expand_shortenkey',
                        side_effect=ShortenKeyDoesNotExist, autospec=True) as m:
            from pyramid.httpexceptions import HTTPNotFound
            self.assertRaises(HTTPNotFound, self._callFUT, request)

        m.assert_called_with('aa')

    def test__matched(self):
        request = testing.DummyRequest()
        request.matchdict['shortenkey'] = 'aa'

        with mock.patch('foomn.views.expand_shortenkey',
                        return_value='http://example.com/', autospec=True) as m:
            response = self._callFUT(request)

        m.assert_called_with('aa')
        self.assertEqual(301, response.code)
        self.assertEqual('http://example.com/', response.location)
