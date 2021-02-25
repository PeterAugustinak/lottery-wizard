# coding=utf-8
"""Unit tests for lottery.py module"""

# local library imports
from src.lottery import Lottery
# standard library imports
import unittest
from unittest.mock import patch
import io


class LottreyTest(unittest.TestCase):
    """Unittest class for testing Lottery class"""

    lottery_en = Lottery(0)
    lottery_sk = Lottery(1)

    def setUp(self):
        pass

    def tearDown(self) -> None:
        pass

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_input_lottery_pool_text_en(self, mock_stdout):
        expected = "How many numbers are in the pool for lottery? (35-100)\n" \
                   " (example: 49)"
        self.lottery_en.print_input_text_lottery_pool()
        assert mock_stdout.getvalue() == f'{expected}\n'

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_input_lottery_pool_text_sk(self, mock_stdout):
        expected = "Z koľkých čísel sa losuje v tejto lotérii? (35-100)\n" \
                   " (príklad: 49)"
        self.lottery_sk.print_input_text_lottery_pool()
        assert mock_stdout.getvalue() == f'{expected}\n'

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_input_amount_of_draw_numbers_text_en(self, mock_stdout):
        expected = "How many numbers is going to be drawn every draw in this lottery? (1-10)\n" \
                         " (example: 6)"
        self.lottery_en.print_input_text_amount_of_draw_numbers()
        assert mock_stdout.getvalue() == f'{expected}\n'

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_input_amount_of_draw_numbers_text_sk(self, mock_stdout):
        expected = "Koľko čísel sa žrebuje v jednom ťahu v tejto lotérií? (1-10)\n" \
                   " (príklad: 6)"
        self.lottery_sk.print_input_text_amount_of_draw_numbers()
        assert mock_stdout.getvalue() == f'{expected}\n'

    #
    # # def test_input_draw_numbers_text(self):
    # #     self.lottery.lang = 0
    # #     self.assertEqual("Please input your 6 numbers from 1 to 55 and press ENTER.\n"
    # #                      f" (example: {re.findall(r'^[0-9][0-9]{6}$')})"

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_input_draws_per_week_text_en(self, mock_stdout):
        expected = "How many draws per week you want to bet?\n" \
                   " (example: 1)"
        self.lottery_en.print_input_text_draws_per_week()
        assert mock_stdout.getvalue() == f'{expected}\n'

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_input_draws_per_week_text_sk(self, mock_stdout):
        expected = "Na koľko ťahov týždenne chceš podať?\n" \
                   " (príklad: 1)"
        self.lottery_sk.print_input_text_draws_per_week()
        assert mock_stdout.getvalue() == f'{expected}\n'

    # VALIDATIONS
    def test_validate_lottery_pool_input(self):
        # range error left
        self.lottery_en.parse_lottery_pool_input('34')
        self.assertTrue(self.lottery_en.get_user_has_no_or_incorrect_answer())

        # range error right
        self.lottery_sk.parse_lottery_pool_input('101')
        self.assertTrue(self.lottery_sk.get_user_has_no_or_incorrect_answer())

        # range error negative
        self.lottery_en.parse_lottery_pool_input('-45')
        self.assertTrue(self.lottery_en.get_user_has_no_or_incorrect_answer())

        # value error - char
        self.lottery_sk.parse_lottery_pool_input('erf')
        self.assertTrue(self.lottery_sk.get_user_has_no_or_incorrect_answer())

        # value error - no char
        self.lottery_sk.parse_lottery_pool_input('')
        self.assertTrue(self.lottery_sk.get_user_has_no_or_incorrect_answer())

        # correct middle
        self.lottery_sk.parse_lottery_pool_input('45')
        self.assertFalse(self.lottery_sk.get_user_has_no_or_incorrect_answer())

        # correct boundary left
        self.lottery_en.parse_lottery_pool_input('35')
        self.assertFalse(self.lottery_en.get_user_has_no_or_incorrect_answer())

        # correct boundary right
        self.lottery_sk.parse_lottery_pool_input('100')
        self.assertFalse(self.lottery_sk.get_user_has_no_or_incorrect_answer())

    def test_validate_amount_of_draw_numbers(self):
        pass

    def test_parse_draw_numbers_input(self):
        pass

    def test_validate_draw_numbers_input(self):
        pass

    def test_validate_draws_per_week_input(self):
        pass

    def test_failed_validation(self):
        pass

    def test_set_numbers_chart(self):
        pass

    def test_set_guessed_table(self):
        pass

