# coding=utf-8
"""The Lottery project"""

# local library import
from texts import texts
# standard library imports
import random
from os import system
from datetime import datetime, timedelta
import msvcrt
# external library imports
from prettytable import PrettyTable
from itertools import islice


class Lottery:
    """Lottery class"""
    lang = None
    # counter for user input (in case of incorrect input only
    user_no_or_incorrect_input = True
    # numbers for lottery
    defined_numbers_for_draw = []
    random_numbers_for_draw = []
    drawn_numbers = []
    # counter of lottery tosses
    draw_counter = 1
    # date
    current_date = None
    draws_per_week = 7
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
    numbers_chart = {}

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
        self.user_inputs()

    def user_inputs(self):
        """This clarifies if user want to use his own numbers or just leave it for random AI choices"""
        # ask user for input numbers till the format of input is correct
        self.input_draw_numbers_text()
        while self.user_no_or_incorrect_input:
            user_numbers_input = input("-> ")
            self.parse_and_validate_input(user_numbers_input)

        self.user_no_or_incorrect_input = True
        # ask user for input draws per week value till the format is correct
        self.input_draws_per_week_text()
        while self.user_no_or_incorrect_input:
            user_draw_per_week_input = input("-> ")
            self.validate_draws_per_week_input(user_draw_per_week_input)

        self.start_lottery()

    def input_draw_numbers_text(self):
        """Prints text explaining how to input numbers for draw"""
        print(f"{texts['intro1'][self.lang]}\n{texts['intro2'][self.lang]}")

    def input_draws_per_week_text(self):
        """Prints text explaining how to input draws per week"""
        print(f"{texts['text_draws_per_input1'][self.lang]}\n{texts['text_draws_per_input2'][self.lang]}")

    def parse_and_validate_input(self, user_input):
        """This will parse and validate user input. If the input is incorrect, back to initial question"""
        try:
            numbers = [int(element) for element in user_input.split() if int(element) in range(1, 50)]
            self.defined_numbers_for_draw = sorted(numbers) if len(numbers) == 6 else self.failed_validation()
            self.user_no_or_incorrect_input = False
        except ValueError:
            self.failed_validation()

    def validate_draws_per_week_input(self, user_input):
        """This validates user defined draws per week input"""
        try:
            self.draws_per_week = int(user_input)
            self.user_no_or_incorrect_input = False
        except ValueError:
            self.failed_validation()

    def failed_validation(self):
        """This prints the reason of incorrect validation and starts user input again"""
        print(f" {texts['val_error'][self.lang]}")

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
            self.draw_counter += 1

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
        Also it creates number chart
        """
        guessed = len(set(numbers_for_draw).intersection(self.drawn_numbers))

        if guessed == 0: self.guessed_table['guessed_zero'][inpt] += 1
        if guessed == 1: self.guessed_table['guessed_one'][inpt] += 1
        if guessed == 2: self.guessed_table['guessed_two'][inpt] += 1
        if guessed == 3: self.guessed_table['guessed_three'][inpt] += 1
        if guessed == 4: self.guessed_table['guessed_four'][inpt] += 1
        if guessed == 5: self.guessed_table['guessed_five'][inpt] += 1
        if guessed == 6: self.guessed_table['guessed_six'][inpt] += 1

        # putting data data into numbers chart
        for number in self.drawn_numbers:
            if number in self.numbers_chart.keys():
                self.numbers_chart[number] += 1
            else:
                self.numbers_chart.update({number: 1})

    def print_results(self):
        """This prints current results"""

        print(self.create_table_input())
        print()
        print(self.create_table_draw())
        print()
        print(self.create_table_stat())
        print()
        print(self.create_table_chart())

    def create_table_input(self):
        """Builds table for input information"""

        table_input = PrettyTable(header=False)

        table_input.add_rows([
            [
                texts['your_nums'][self.lang].upper(),
                f"{self.defined_numbers_for_draw}        "
            ],
            [
                texts['random_nums'][self.lang].upper(),
                self.random_numbers_for_draw
            ]
            ])

        table_input.align = "l"
        return table_input

    def create_table_draw(self):
        """Builds table for drawing information"""

        table_draw = PrettyTable(header=False)

        table_draw.add_rows([
            [
                texts['draws_p_w'][self.lang].upper(),
                self.draws_per_week
            ],
            [
                texts['date'][self.lang].upper(),
                self.count_date()
            ],
            [
                texts['draw'][self.lang],
                f"{self.draw_counter:,}                          "
            ],
            [
                texts['drawn_nums'][self.lang].upper(),
                self.drawn_numbers]]
        )

        table_draw.align = "l"
        return table_draw

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

    def create_table_chart(self):
        """This creates table with numbers chart"""
        table_chart = PrettyTable()

        table_chart.title = texts['chart_title'][self.lang]
        table_chart.field_names = [texts['chart_top_nm'][self.lang],
                                   texts['chart_top_val'][self.lang],
                                   texts['chart_down_nm'][self.lang],
                                   texts['chart_down_val'][self.lang]]

        table_chart.align[texts['chart_top_val'][self.lang]] = "r"
        table_chart.align[texts['chart_down_val'][self.lang]] = "r"

        sorted_chart_top = dict(sorted(self.numbers_chart.items(), key=lambda item: item[1], reverse=True))
        sorted_chart_down = dict(sorted(self.numbers_chart.items(), key=lambda item: item[1]))

        top = list(islice(sorted_chart_top.items(), 0, 6))
        down = list(islice(sorted_chart_down.items(), 0, 6))

        for n_top, n_down in zip(top, down[::-1]):
            table_chart.add_row([n_top[0], n_top[1], n_down[0], n_down[1]])

        return table_chart

    def count_date(self):
        """Counts passing the time by weeks"""

        if self.current_date:
            next_date = self.current_date + timedelta(days=7) if self.draw_counter % self.draws_per_week == 0 \
                else self.current_date
        else:
            self.current_date = datetime.today()
            next_date = self.current_date

        current_week_year = datetime.date(next_date).isocalendar()
        week = current_week_year[1] if current_week_year[1] > 9 else f"0{current_week_year[1]}"
        year = current_week_year[0]

        self.current_date = next_date
        return f"{week}/{year}"

    def count_percentage(self, correct_guesses):
        """This counts percentage value of how many guess of the particular number of total draw was success"""
        return round(100 / self.draw_counter * correct_guesses, 3)

    def lottery_won(self):
        """In case of 6 numbers of 6 was guessed correctly - means lottery is won, the tossing will stop"""
        print()
        print(f"!!! {texts['won1'][self.lang]}{self.draw_counter}!!!")
        # print(f"{texts['your_was'][self.lang]} {self.defined_numbers_for_draw} {texts['drawn_was'][self.lang]} "
        # f"{self.drawn_numbers}!!!")
        print(f"{texts['won2'][self.lang]} {self.count_years()} {texts['won3'][self.lang]}")

    def count_years(self):
        """This counts the time evaluated to win"""
        return round(self.draw_counter / 52, 0)


Lottery().language_input()
