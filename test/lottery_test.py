# coding=utf-8
"""Unit tests for lottery.py module"""

# local library imports
from src.lottery import Lottery
# standard library imports
import unittest


class LottreyTest(unittest.TestCase):
    """Unittest class for testing Lottery class"""

    def setUp(self):
        pass

    def tearDown(self) -> None:
        pass

    def test_set_number_chart(self):
        """testing set_number_chart() method"""
        self.numbers_chart = None
        Lottery().set_numbers_chart(1)
        self.assertEqual(1, len(self.numbers_chart))



