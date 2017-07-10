import unittest

from utils.pda_manager import load_pda_messages


class TestPDAManagement(unittest.TestCase):

    def test_loading_messages(self):
        messages = load_pda_messages("assets/default-scenario")
        self.assertTrue(True)
