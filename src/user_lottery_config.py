# coding=utf-8

# local library imports
from texts import texts
from common import pick_random_numbers


class UserLotteryConfig:
    """Class for setting user defined lottery where the output is lottery settings"""

    def __init__(self, lang):
        self.lang = lang
        # counter for user input (in case of incorrect input only
        self._user_has_no_or_incorrect_answer = True
        # lottery config defined by user
        self.lottery_pool = None
        self.amount_of_draw_numbers = None
        self.lottery_numbers = None
        self.draws_per_week = None

    def get_user_has_no_or_incorrect_answer(self):
        """For testing purposes"""
        return self._user_has_no_or_incorrect_answer

    # USER INPUTS HANDLING BEFORE LOTTERY CAN START ###
    def user_inputs(self):
        # how many numbers will have lottery
        self.print_input_text_lottery_pool()
        while self._user_has_no_or_incorrect_answer:
            self.parse_lottery_pool_input(input("-> "))

        self._user_has_no_or_incorrect_answer = True
        # how many numbers is going to be drawn
        self.print_input_text_amount_of_draw_numbers()
        while self._user_has_no_or_incorrect_answer:
            self.parse_amount_of_draw_numbers(input("-> "))

        self._user_has_no_or_incorrect_answer = True
        # define user numbers for draw
        self.print_input_text_define_numbers()
        while self._user_has_no_or_incorrect_answer:
            self.parse_user_lottery_numbers_input(input("-> "))

        self._user_has_no_or_incorrect_answer = True
        # ask user for input draws per week value till the format is correct
        self.print_input_text_draws_per_week()
        while self._user_has_no_or_incorrect_answer:
            self.parse_draws_per_week_input(input("-> "))

    # USER INPUTS TEXTS
    def print_input_text_lottery_pool(self):
        print(f"{texts['text_pool_input1'][self.lang]}\n{texts['text_pool_input2'][self.lang]}")

    def print_input_text_amount_of_draw_numbers(self):
        print(f"{texts['input_amount_of_draw1'][self.lang]}\n{texts['input_amount_of_draw2'][self.lang]}")

    def print_input_text_define_numbers(self):
        random_numbers = pick_random_numbers(self.lottery_pool, self.amount_of_draw_numbers)
        text = f"{texts['intro1-1'][self.lang]}{self.amount_of_draw_numbers}{texts['intro1-2'][self.lang]}" \
               f"{self.lottery_pool}{texts['intro1-3'][self.lang]}\n" \
               f"{texts['intro1-4'][self.lang]}{' '.join(map(str, sorted(random_numbers)))})"
        print(text)

    def print_input_text_draws_per_week(self):
        print(f"{texts['text_draws_per_input1'][self.lang]}\n{texts['text_draws_per_input2'][self.lang]}")

    # PARSERS AND VALIDATORS OF USER INPUTS

    def parse_lottery_pool_input(self, user_input):
        try:
            parsed_user_input = int(user_input)
            self.validate_lottery_pool_input(parsed_user_input)
        except ValueError:
            self.failed_validation('val_error_int2')

    def validate_lottery_pool_input(self, parsed_user_input):
        if 35 <= parsed_user_input <= 100:
            self.lottery_pool = parsed_user_input
            self._user_has_no_or_incorrect_answer = False
        else:
            self.failed_validation('val_error_range')

    def parse_amount_of_draw_numbers(self, user_input):
        try:
            parsed_user_input = int(user_input)
            self.validate_amount_of_draw_numbers(parsed_user_input)
        except ValueError:
            self.failed_validation('val_error_int2')

    def validate_amount_of_draw_numbers(self, parsed_user_input):
        if 1 <= parsed_user_input <= 10:
            self.amount_of_draw_numbers = parsed_user_input
            self._user_has_no_or_incorrect_answer = False
        else:
            self.failed_validation('val_error_range')

    def parse_user_lottery_numbers_input(self, user_input):
        try:
            parsed_user_input = [int(element) for element in user_input.split()
                                 if int(element) in range(1, self.lottery_pool + 1)]
            self.validate_user_lottery_numbers_input(parsed_user_input)
        except ValueError:
            self.failed_validation('val_error_int')

    def validate_user_lottery_numbers_input(self, parsed_user_input):
        if len(parsed_user_input) == self.amount_of_draw_numbers:
            self.lottery_numbers = sorted(parsed_user_input)
            self._user_has_no_or_incorrect_answer = False
        else:
            self.failed_validation('val_error_count')

    def parse_draws_per_week_input(self, user_input):
        try:
            self.draws_per_week = int(user_input)
            self._user_has_no_or_incorrect_answer = False
        except ValueError:
            self.failed_validation('val_error_int')

    def failed_validation(self, val_error):
        self._user_has_no_or_incorrect_answer = True
        print(f" {texts[val_error][self.lang]}")

