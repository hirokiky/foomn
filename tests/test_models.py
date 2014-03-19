import unittest


class TestURLMapping(unittest.TestCase):
    def _getTarget(self):
        from foomn.models import URLMapping
        return URLMapping

    def _makeOne(self, *args, **kwargs):
        return self._getTarget()(*args, **kwargs)

    def test_validate_region_code__invalid(self):
        self.assertRaises(ValueError, self._makeOne, region_code='&')

    def test_validate_region_code__valid(self):
        target = self._makeOne(region_code='b')
        self.assertEqual('b', target.region_code)

    def test_validate_url__invalid(self):
        self.assertRaises(ValueError, self._makeOne, url='http://')
        self.assertRaises(ValueError, self._makeOne, url='')
        self.assertRaises(ValueError, self._makeOne, url='news://example.com/')
        self.assertRaises(ValueError, self._makeOne, url='http://foo.mn/')
        self.assertRaises(ValueError, self._makeOne, url='http://foo.mn/path/')
        self.assertRaises(ValueError, self._makeOne, url='test.com')
        self.assertRaises(ValueError, self._makeOne, url='')

    def test_validate_url__valid(self):
        target = self._makeOne(url='http://example.com/')
        self.assertEqual('http://example.com/', target.url)
        target = self._makeOne(url='https://example.com/')
        self.assertEqual('https://example.com/', target.url)
        target = self._makeOne(url='ftp://example.com/')
        self.assertEqual('ftp://example.com/', target.url)
        target = self._makeOne(url='ftps://example.com/')
        self.assertEqual('ftps://example.com/', target.url)
        target = self._makeOne(url='http://www.example.com/')
        self.assertEqual('http://www.example.com/', target.url)
        target = self._makeOne(url='http://example.com/path/')
        self.assertEqual('http://example.com/path/', target.url)
        target = self._makeOne(url='http://with-hyphens.com/')
        self.assertEqual('http://with-hyphens.com/', target.url)
        target = self._makeOne(url='http://example.com/?withquery=1')
        self.assertEqual('http://example.com/?withquery=1', target.url)
        target = self._makeOne(url='http://example.com?withquery=1')
        self.assertEqual('http://example.com?withquery=1', target.url)
        target = self._makeOne(url='http://example.com:8080/')
        self.assertEqual('http://example.com:8080/', target.url)
        target = self._makeOne(url='http://example.com/%e5%bf%8d')
        self.assertEqual('http://example.com/%e5%bf%8d', target.url)
