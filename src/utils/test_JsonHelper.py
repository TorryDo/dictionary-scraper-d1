from unittest import TestCase

from src.utils.FileHelper import FileHelper
from src.utils.JsonHelper import JsonHelper


class TestJsonHelper(TestCase):
    _test_json: str = FileHelper.read_file('../../assets/data/test_json.txt')

    def test_str2dict(self):
        cock: dict = JsonHelper.str2dict(self._test_json)
        expect_true = cock['en'][0]['language'] == 'English'

        self.assertTrue(expect_true)

    def test_dict2json(self):
        _test_dict: dict = JsonHelper.str2dict(self._test_json)
        result = JsonHelper.dict2json(_test_dict)

        self.assertTrue(result != '' and result is not None)

    def test_is_json(self):
        expect_false = JsonHelper.is_json(self._test_json)
        self.assertFalse(expect_false)
