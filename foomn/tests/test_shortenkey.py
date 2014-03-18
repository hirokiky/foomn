import unittest


def setUpModule():
    from foomn.testing import setup_models
    setup_models()


def tearDownModule():
    from foomn.testing import teardown_models
    teardown_models()


class TestMappingCodeToId(unittest.TestCase):
    def _callFUT(self, *args, **kwargs):
        from foomn.shortenkey import mapping_code_to_id
        return mapping_code_to_id(*args, **kwargs)

    def test__valid(self):
        self.assertEqual(1, self._callFUT('1'))
        self.assertEqual(61, self._callFUT('Z'))
        self.assertEqual(62, self._callFUT('10'))

    def test__invalid_digit_character(self):
        from foomn.shortenkey import InvalidShortenKey
        self.assertRaises(InvalidShortenKey, self._callFUT, '$')
        self.assertRaises(InvalidShortenKey, self._callFUT, '-')
        self.assertRaises(InvalidShortenKey, self._callFUT, 'Ａ')


class TestMappingIdToCode(unittest.TestCase):
    def _callFUT(self, *args, **kwargs):
        from foomn.shortenkey import mapping_id_to_code
        return mapping_id_to_code(*args, **kwargs)

    def test__valid(self):
        self.assertEqual('1', self._callFUT(1))
        self.assertEqual('Z', self._callFUT(61))
        self.assertEqual('10', self._callFUT(62))

    def test__not_int(self):
        self.assertRaises(ValueError, self._callFUT, 'a')
        self.assertRaises(ValueError, self._callFUT, 2.8)

    def test__not_positive_value(self):
        self.assertRaises(ValueError, self._callFUT, 0)
        self.assertRaises(ValueError, self._callFUT, -1)


class TestParseShortenkey(unittest.TestCase):
    def _callFUT(self, *args, **kwargs):
        from foomn.shortenkey import parse_shortenkey
        return parse_shortenkey(*args, **kwargs)

    def test__invalid_shortenkey(self):
        from foomn.shortenkey import InvalidShortenKey
        self.assertRaises(InvalidShortenKey, self._callFUT, 'A')  # Too short
        self.assertRaises(InvalidShortenKey, self._callFUT, '00&')  # Invalid character

    def test__valid(self):
        self.assertEqual(('A', '0'), self._callFUT('A0'))
        self.assertEqual(('t', 'ritsu'), self._callFUT('tritsu'))


class TestExpandShortenKey(unittest.TestCase):
    def _callFUT(self, *args, **kwargs):
        from foomn.shortenkey import expand_shortenkey
        return expand_shortenkey(*args, **kwargs)

    def tearDown(self):
        import transaction
        transaction.abort()

    def test__key_matched(self):
        from foomn import models
        mapping = models.URIMapping(mapping_id=1,
                                    region_code='0',
                                    uri='http://example.com/')
        models.DBSession.add(mapping)
        models.DBSession.flush()

        actual = self._callFUT('01')

        self.assertEqual('http://example.com/', actual)

    def test__invalid_shorten_key(self):
        from foomn.shortenkey import InvalidShortenKey
        self.assertRaises(InvalidShortenKey, self._callFUT, '0')

    def test__mapping_does_not_exist(self):
        from foomn.shortenkey import ShortenKeyDoesNotExist
        self.assertRaises(ShortenKeyDoesNotExist, self._callFUT, '01')
