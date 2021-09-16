# coding=utf-8
"""LotteryEngine Class"""

# standard library imports
from os import system
# local library import
from lottery_cmd_output import LotteryCmdOutput
from texts import texts
from common import pick_random_numbers


class LotteryEngine:
    """LotteryEngine runs lottery drawing and statistics based on user
     configuration input"""

    def __init__(self, language, lottery_pool, amount_of_draw_numbers,
                 lottery_numbers, draws_per_week):
        self.lang = language
        self.lottery_pool = lottery_pool
        self.amount_of_draw_numbers = amount_of_draw_numbers
        self.user_defined_numbers = lottery_numbers
        self.draws_per_week = draws_per_week
        # dicts to store current situation after every draw
        self._guessed_table = {}
        self._numbers_chart = {}
        # numbers for lottery
        self._random_numbers_for_draw = []
        self._drawn_numbers = []
        # counter of lottery tosses
        self._draw_counter = 0
        # initialize object for building tables for cmd output
        self.cmd_output = LotteryCmdOutput(language, draws_per_week)
        self._user_defined_numbers_won = False
        self._random_numbers_won = False

    # TABLES SETTERS
    def set_guessed_table(self):
        """Sets table to store how much time the particular nnumber was
         guessed based on amount of numbers to draw"""

        for number in range(0, self.amount_of_draw_numbers + 1):
            # {numbers guessed in round: ([user def nums, first guess in draw],
            # [random nums, first guessed in draw)]
            self._guessed_table.update({number: ([0, 0], [0, 0])})

    def set_numbers_chart(self):
        """Sets table for numbers chart baesed on lottery pool value"""
        for number in range(1, self.lottery_pool + 1):
            self._numbers_chart.update({number: 0})

    # START OF LOTTERY DRAWINGS
    def start_lottery(self):
        self.set_guessed_table()
        self.set_numbers_chart()

        while not self._user_defined_numbers_won:
            self._draw_counter += 1
            self._random_numbers_for_draw = pick_random_numbers(
                self.lottery_pool, self.amount_of_draw_numbers)
            self._drawn_numbers = pick_random_numbers(
                self.lottery_pool, self.amount_of_draw_numbers)
            self.evaluate_round(self.user_defined_numbers, 0)
            self.evaluate_round(self._random_numbers_for_draw, 1)

            system('cls')
            self.print_cmd_output()

        self.lottery_won()

    def evaluate_round(self, numbers_for_draw, inpt):
        """
        This will compare numbers for draw against drawn numbers for the round
        numbers_for_draw - either user_defined_numbers or
        _random_numbers_for_draw
        inpt: 0 -> user defined draw numbers
        inpt: 1 -> random defined draw numbers
        Also it shows online output
        """
        guessed = len(set(numbers_for_draw).intersection(self._drawn_numbers))
        self._guessed_table[guessed][inpt][0] += 1

        # check for win - if all numbers was guessed
        guessed_all = self._guessed_table[self.amount_of_draw_numbers]
        if guessed_all[inpt][0] == 1:
            if inpt == 0:
                self._user_defined_numbers_won = True
            if inpt == 1:
                self._random_numbers_won = self._random_numbers_for_draw

        # check if this number of guessed numbers is first time
        if self._guessed_table[guessed][inpt][1] > 0:
            pass
        # if yes, put draw # too to know in what draw happend first succes
        else:
            self._guessed_table[guessed][inpt][1] = self._draw_counter

        # putting data into numbers chart
        for number in self._drawn_numbers:
            self._numbers_chart[number] += 1

    def print_cmd_output(self):
        """This prints current results"""

        print(self.cmd_output.create_table_input(self.user_defined_numbers,
                                                 self._random_numbers_for_draw,
                                                 self.draws_per_week, ))
        print()
        print(self.cmd_output.create_table_draw(self._draw_counter,
                                                self._drawn_numbers))
        print()
        print(texts['note'][self.lang])
        print(self.cmd_output.create_table_stat(self._guessed_table,
                                                self._draw_counter))
        print()
        print(self.cmd_output.create_table_chart(self.amount_of_draw_numbers,
                                                 self._numbers_chart))
        print()
        if self._random_numbers_won:
            draw = self._guessed_table[self.amount_of_draw_numbers][1][1]
            self.cmd_output.random_numbers_won(self._random_numbers_won, draw)

    def lottery_won(self):
        print()
        print(f"!!! {texts['won1'][self.lang]}{self._draw_counter}!!!")
        print(f"{texts['won-date']} {self.cmd_output.current_date}")
        # print(f"{texts['your_was'][self.lang]}
        # {self._defined_numbers_for_draw} {texts['drawn_was'][self.lang]} "
        # f"{self._drawn_numbers}!!!")
        print(f"{texts['won2'][self.lang]} {self.count_years()} "
              f"{texts['won3'][self.lang]}")

    def count_years(self):
        """This counts the time evaluated to win"""
        return round(self._draw_counter / 52, 0)
