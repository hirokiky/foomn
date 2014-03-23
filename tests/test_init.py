import unittest
from unittest import mock


class TestInitSettings(unittest.TestCase):
    def _callFUT(self, *args, **kwargs):
        from foomn import init_settings
        return init_settings(*args, **kwargs)

    @mock.patch('foomn.set_settings', autospec=True)
    def test__init(self, set_settings_mock):
        import os
        here = os.path.join(os.path.dirname(__file__), 'fixtures')
        file_path = os.path.join(here, 'test_ini.ini')

        with mock.patch.dict('foomn.os.environ', {'PYRAMID_SETTINGS': file_path}):
            self._callFUT()
        set_settings_mock.assert_called_with({'leader': 'Ritsu Tainaka',
                                              'here': here,
                                              '__file__': file_path})
