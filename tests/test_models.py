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
