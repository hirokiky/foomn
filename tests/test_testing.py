import unittest


class TestOverrideSettings(unittest.TestCase):
    def _makeOne(self, **kwargs):
        from foomn.testing import override_settings
        return override_settings(**kwargs)

    def test__as_with(self):
        from foomn import get_settings
        target = self._makeOne(override_settings__with='with_testing')
        with target:
            self.assertEqual('with_testing', get_settings()['override_settings__with'])

        with self.assertRaises(KeyError):
            get_settings()['override_settings__with']

    def test__as_function_decorator(self):
        from foomn import get_settings
        target = self._makeOne(override_settings__func_dec='func_dec_testing')

        def wrapped():
            self.assertEqual('func_dec_testing', get_settings()['override_settings__func_dec'])

        target(wrapped)()

        with self.assertRaises(KeyError):
            get_settings()['override_settings__func_dec']
