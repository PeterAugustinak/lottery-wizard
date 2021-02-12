# coding=utf-8
"""The Lottery project"""

# local library import
from texts import texts
# standard library imports
import random
from os import system
import msvcrt
# external library imports
from prettytable import PrettyTable


class Lottery:
    """Lottery class"""
    lang = None
    # counter for user input (in case of incorrect input only
    user_incorrect_input = False
    # numbers for lottery
    defined_numbers_for_draw = []
    random_numbers_for_draw = []
    drawn_numbers = []
    # counter of lottery tosses
    toss_counter = 1
    # storing sucessfull guesses after every draw
    guessed_table = {
        'guessed_zero': [0, 0],
        'guessed_one': [0, 0],
        'guessed_two': [0, 0],
        'guessed_three': [0, 0],
        'guessed_four': [0, 0],
        'guessed_five': [0, 0],
        'guessed_six': [0, 0]
    }

    def __init__(self):
        pass

    # USER INPUT BEFORE LOTTERY CAN START ###
    def language_input(self):
        """User will at first select language for the Lottery app"""
        system('cls')
        print("1. ENG\n"
              "2. SVK\n")

        lang_input = msvcrt.getch()
        # 0 = English, 1 = Slovak
        try:
            if int(lang_input) != 2:
                self.lang = 0
            else:
                self.lang = 1
        except ValueError:
            self.lang = 0

        system('cls')
        self.numbers_input()

    def numbers_input(self):
        """This clarifies if user want to use his own numbers or just leave it for random AI choices"""
        if not self.user_incorrect_input:
            self.intro_text()
        user_input = input("-> ")

        self.defined_numbers_for_draw = sorted(self.parse_and_validate_input(user_input))
        self.start_lottery()

    def intro_text(self):
        """Prints intro navugation text"""
        # this is in separate method because we don't wanna to print it again after every invalid user input.
        print(f"{texts['intro1'][self.lang]}\n{texts['intro2'][self.lang]}")

    def parse_and_validate_input(self, user_input):
        """This will parse and validate user input. If the input is incorrect, back to initial question"""
        try:
            numbers = [int(element) for element in user_input.split() if int(element) in range(1, 50)]
            return numbers if len(numbers) == 6 else self.failed_validation()
        except ValueError:
            self.failed_validation()

    def failed_validation(self):
        """This prints the reason of incorrect validation and starts user input again"""
        print(texts['val_error'][self.lang])
        self.user_incorrect_input = True
        self.numbers_input()

    # START OF LOTTERY DRAWINGS ... ###
    def start_lottery(self):
        """This will toss lottery"""
        while self.guessed_table['guessed_six'][0] == 0 and self.guessed_table['guessed_six'][1] == 0:
            self.random_numbers_for_draw = sorted(self.random_numbers())
            self.drawn_numbers = sorted(self.random_numbers())
            self.evaluate_round(self.defined_numbers_for_draw, 0)
            self.evaluate_round(self.random_numbers_for_draw, 1)

            system('cls')
            self.print_results()
            self.toss_counter += 1

        self.lottery_won()

    @staticmethod
    def random_numbers():
        """Picks 6 random numbers instead of the user"""
        return [random.randrange(1, 50) for _ in range(6)]

    def evaluate_round(self, numbers_for_draw, inpt):
        """
        This will compare numbers for deaw against drawn numbers for the round
        inpt: 0 -> user defined numbers
        inpt: 1 -> random defined numbers
        """
        guessed = len(set(numbers_for_draw).intersection(self.drawn_numbers))

        if guessed == 0: self.guessed_table['guessed_zero'][inpt] += 1
        if guessed == 1: self.guessed_table['guessed_one'][inpt] += 1
        if guessed == 2: self.guessed_table['guessed_two'][inpt] += 1
        if guessed == 3: self.guessed_table['guessed_three'][inpt] += 1
        if guessed == 4: self.guessed_table['guessed_four'][inpt] += 1
        if guessed == 5: self.guessed_table['guessed_five'][inpt] += 1
        if guessed == 6: self.guessed_table['guessed_six'][inpt] += 1

    def print_results(self):
        """This prints current results"""

        table_info = self.create_table_info()
        table_stat = self.create_table_stat()

        print(table_info)
        print()
        print(table_stat)

    def create_table_info(self):
        """Builds table for drawing information"""

        table_info = PrettyTable(header=False)

        table_info.add_rows([
            [
                texts['draw'][self.lang],
                f"{self.toss_counter:,}                          "
            ],
            [
                texts['your_nums'][self.lang].upper(),
                self.defined_numbers_for_draw
            ],
            [
                texts['random_nums'][self.lang].upper(),
                self.random_numbers_for_draw
            ],
            [
                texts['drawn_nums'][self.lang].upper(),
                self.drawn_numbers]]
        )

        table_info.align = "l"
        return table_info

    def create_table_stat(self):
        """Builds table for drawing stats"""
        table_stat = PrettyTable()

        table_stat.field_names = [texts['table_f1'][self.lang],
                                  texts['table_f2'][self.lang],
                                  texts['table_f3'][self.lang],
                                  texts['table_f4'][self.lang],
                                  texts['table_f5'][self.lang]]

        table_stat.align[texts['table_f1'][self.lang]] = "l"
        table_stat.align[texts['table_f2'][self.lang]] = "r"
        table_stat.align[texts['table_f3'][self.lang]] = "r"
        table_stat.align[texts['table_f4'][self.lang]] = "r"
        table_stat.align[texts['table_f5'][self.lang]] = "r"

        for i, key in zip(range(len(self.guessed_table)), self.guessed_table.keys()):
            if i == 0:
                nm = 'num'
            elif i == 1:
                nm = 'nums'
            else:
                nm = 'numss'

            table_stat.add_row(
                [
                    f"{i} {texts[nm][self.lang]}",
                    self.guessed_table[key][0],
                    self.count_percentage(self.guessed_table[key][0]),
                    self.guessed_table[key][1],
                    self.count_percentage(self.guessed_table[key][1]),
                ]
             )

        return table_stat

    def count_years(self):
        """This counts the time evaluated to win"""
        return round(self.toss_counter / 52, 0)

    def count_percentage(self, correct_guesses):
        """This counts percentage value of how many guess of the particular number of total draw was success"""
        return round(100 / self.toss_counter * correct_guesses, 3)

    def lottery_won(self):
        """In case of 6 numbers of 6 was guessed correctly - means lottery is won, the tossing will stop"""
        print()
        print(f"!!! {texts['won1'][self.lang]}{self.toss_counter}!!!")
        # print(f"{texts['your_was'][self.lang]} {self.defined_numbers_for_draw} {texts['drawn_was'][self.lang]} "
        # f"{self.drawn_numbers}!!!")
        print(f"{texts['won2'][self.lang]} {self.count_years()} {texts['won3'][self.lang]}")


Lottery().language_input()
