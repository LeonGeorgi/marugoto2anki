import unittest

from util.string_utils import convert_lesson, convert_pronunciation, convert_pronunciation_to_kana


class TestStringUtils(unittest.TestCase):
    def test_convert_lesson(self):
        self.assertEqual(convert_lesson("17"), '17')
        self.assertEqual(convert_lesson("13"), '13')
        self.assertEqual(convert_lesson("9ス"), '9')
        self.assertEqual(convert_lesson("８ス"), '8')

    def test_convert_pronunciation(self):
        self.assertEqual(convert_pronunciation('しりあ7う'), 'しりあ￢う')
        self.assertEqual(convert_pronunciation('あいている0'), 'あいている￣')

    def test_convert_pronunciation_to_kana(self):
        self.assertEqual(convert_pronunciation_to_kana('しりあ7う'), 'しりあう')
        self.assertEqual(convert_pronunciation_to_kana('あいている0'), 'あいている')

