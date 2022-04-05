import unittest
from unittest import mock

from util.user_input import ask_user_for_language


class TestUserInput(unittest.TestCase):
    @mock.patch('util.user_input.input', create=True)
    def test_select_language(self, mocked_input):
        mocked_input.side_effect = ['de', 'en']
        self.assertEqual(ask_user_for_language({'de', 'fr'}), 'de')
        self.assertEqual(ask_user_for_language({'fr'}), 'fr')
        self.assertRaises(Exception, lambda: ask_user_for_language({'de', 'fr'}))
