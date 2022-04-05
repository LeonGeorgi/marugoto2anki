import unittest

from util.string_utils import convert_lesson


class TestStringUtils(unittest.TestCase):
    def test_convert_lesson(self):
        self.assertEqual(convert_lesson("17"), 17)
        self.assertEqual(convert_lesson("13"), 13)
        self.assertEqual(convert_lesson("9ス"), 9)
        self.assertEqual(convert_lesson("８ス"), 8)
