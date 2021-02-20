# coding=utf-8
"""Unit tests for lottery.py module"""

# local library imports
from src.lottery import Lottery
# standard library imports
import unittest
import re


class LottreyTest(unittest.TestCase):
    """Unittest class for testing Lottery class"""

    lottery = Lottery()
    def setUp(self):
        pass

    def tearDown(self) -> None:
        pass

    def test_input_lottery_pool_text(self):
        self.lottery.lang = 0
        self.assertEqual("How many numbers are in the pool for lottery? (35-100)\n"
                         " (example: 49)",
                         self.lottery.input_lottery_pool_text())

        self.lottery.lang = 1
        self.assertEqual("Z koľkých čísel sa losuje v tejto lotérii? (35-100)\n"
                         " (príklad: 49)",
                         self.lottery.input_lottery_pool_text())

    def test_input_amount_of_draw_numbers_text(self):
        self.lottery.lang = 0
        self.assertEqual("How many numbers is going to be drawn every draw in this lottery? (1-10)\n"
                         " (example: 6)",
                         self.lottery.input_amount_of_draw_numbers_text())

        self.lottery.lang = 1
        self.assertEqual("Koľko čísel sa žrebuje v jednom ťahu v tejto lotérií? (1-10)\n"
                         " (príklad: 6)",
                         self.lottery.input_amount_of_draw_numbers_text())

    # def test_input_draw_numbers_text(self):
    #     self.lottery.lang = 0
    #     self.assertEqual("Please input your 6 numbers from 1 to 55 and press ENTER.\n"
    #                      f" (example: {re.findall(r'^[0-9][0-9]{6}$')})"

    def test_input_draws_per_week_text(self):
        self.lottery.lang = 0
        self.assertEqual("How many draws per week you want to bet?\n"
                         " (example: 1)",
                         self.lottery.input_draws_per_week_text())

        self.lottery.lang = 1
        self.assertEqual("Na koľko ťahov týždenne chceš podať?\n"
                         " (príklad: 1)",
                         self.lottery.input_draws_per_week_text())





