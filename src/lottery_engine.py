# coding=utf-8
"""LotteryEngine Class"""

# local library import
from texts import texts
from common import pick_random_numbers
# standard library imports
from os import system
from datetime import datetime, timedelta
# external library imports
from prettytable import PrettyTable
from itertools import islice


class LotteryEngine:
    """LotteryEngine runs lottery drawing and statistics based on user configuration input"""

    def __init__(self, language, lottery_pool, amount_of_draw_numbers, lottery_numbers, draws_per_week):
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
        # date
        self._current_date = None
        self._draws_per_week = None

    # TABLES SETTERS
    def set_guessed_table(self):
        """Sets table to store how much time the particular nnumber was guessed based on amount of
        numbers to draw"""
        for number in range(0, self.amount_of_draw_numbers + 1):
            # {numbers guessed in round: ([user def nums, first guess in draw], [random nums, first guessed in draw)]
            self._guessed_table.update({number: ([0, 0], [0, 0])})

    def set_numbers_chart(self):
        """Sets table for numbers chart baesed on lottery pool value"""
        for number in range(1, self.lottery_pool + 1):
            self._numbers_chart.update({number: 0})

    # START OF LOTTERY DRAWINGS
    def start_lottery(self):
        self.set_guessed_table()
        self.set_numbers_chart()

        guessed_all = self._guessed_table[self.amount_of_draw_numbers]
        while guessed_all[0][0] == 0 and guessed_all[1][0] == 0:
            self._draw_counter += 1
            self._random_numbers_for_draw = pick_random_numbers(self.lottery_pool, self.amount_of_draw_numbers)
            self._drawn_numbers = pick_random_numbers(self.lottery_pool, self.amount_of_draw_numbers)
            self.evaluate_round(self.user_defined_numbers, 0)
            self.evaluate_round(self._random_numbers_for_draw, 1)

            system('cls')
            self.print_results()

        self.lottery_won()

    def evaluate_round(self, numbers_for_draw, inpt):
        """
        This will compare numbers for draw against drawn numbers for the round
        inpt: 0 -> user defined draw numbers
        inpt: 1 -> random defined draw numbers
        Also it creates number chart
        """
        guessed = len(set(numbers_for_draw).intersection(self._drawn_numbers))
        self._guessed_table[guessed][inpt][0] += 1

        # check if this number of guessed numbers is first time
        if self._guessed_table[guessed][inpt][1] > 0:
            pass
        # if yes, put draw # too to know in what draw happend first succes
        else:
            self._guessed_table[guessed][inpt][1] = self._draw_counter

        # putting data data into numbers chart
        for number in self._drawn_numbers:
            self._numbers_chart[number] += 1

    def print_results(self):
        """This prints current results"""

        print(self.create_table_input())
        print()
        print(self.create_table_draw())
        print()
        print(texts['note'][self.lang])
        print(self.create_table_stat())
        print()
        print(self.create_table_chart())

    def create_table_input(self):
        """Builds table for input information"""

        table_input = PrettyTable(header=False)

        table_input.add_rows([
            [
                texts['your_nums'][self.lang].upper(),
                f"{' '.join(map(str, self.user_defined_numbers))}        "
            ],
            [
                texts['random_nums'][self.lang].upper(),
                ' '.join(map(str, self._random_numbers_for_draw))
            ],
            [
                texts['draws_p_w'][self.lang].upper(),
                self._draws_per_week
            ],
        ])

        table_input.align = "l"
        return table_input

    def create_table_draw(self):
        """Builds table for drawing information"""

        table_draw = PrettyTable(header=False)

        table_draw.add_rows([
            [
                texts['date'][self.lang].upper(),
                self.count_date()
            ],
            [
                texts['draw'][self.lang],
                f"{self._draw_counter:,}                         "
            ],
            [
                texts['drawn_nums'][self.lang].upper(),
                ' '.join(map(str, self._drawn_numbers))]]
        )

        table_draw.align = "l"
        return table_draw

    def create_table_stat(self):
        """Builds table for drawing stats"""
        table_stat = PrettyTable()
        table_stat.title = texts['tab_title_stat'][self.lang]

        table_stat.field_names = [texts['table_f1'][self.lang],
                                  texts['table_f2'][self.lang],
                                  texts['table_f3'][self.lang],
                                  texts['table_f4'][self.lang],
                                  texts['table_f5'][self.lang],
                                  texts['table_f6'][self.lang],
                                  texts['table_f7'][self.lang]
                                  ]

        table_stat.align[texts['table_f1'][self.lang]] = "l"
        table_stat.align[texts['table_f2'][self.lang]] = "r"
        table_stat.align[texts['table_f3'][self.lang]] = "r"
        table_stat.align[texts['table_f4'][self.lang]] = "r"
        table_stat.align[texts['table_f5'][self.lang]] = "r"
        table_stat.align[texts['table_f6'][self.lang]] = "r"
        table_stat.align[texts['table_f7'][self.lang]] = "r"

        for i, key in zip(range(len(self._guessed_table)), self._guessed_table.keys()):
            if i == 0:
                nm = 'num'
            elif i == 1:
                nm = 'nums'
            else:
                nm = 'numss'

            guess_num = self._guessed_table[key]
            table_stat.add_row(
                [
                    f"{i} {texts[nm][self.lang]}",
                    guess_num[0][0],
                    f"#{guess_num[0][1] if guess_num[0][1] > 0 else '-'}",
                    self.count_percentage(guess_num[0][0]),
                    guess_num[1][0],
                    f"#{guess_num[1][1] if guess_num[1][1] > 0 else '-'}",
                    self.count_percentage(self._guessed_table[key][1][0]),
                ]
             )

        return table_stat

    def create_table_chart(self):
        """This creates table with numbers chart"""
        table_chart = PrettyTable()

        table_chart.title = f"TOP {self.amount_of_draw_numbers}{texts['tab_title_chart'][self.lang]}"
        table_chart.field_names = [texts['chart_top_nm'][self.lang],
                                   texts['chart_top_val'][self.lang],
                                   texts['chart_down_nm'][self.lang],
                                   texts['chart_down_val'][self.lang]]

        table_chart.align[texts['chart_top_val'][self.lang]] = "r"
        table_chart.align[texts['chart_down_val'][self.lang]] = "r"

        sorted_chart_top = dict(sorted(self._numbers_chart.items(), key=lambda item: item[1], reverse=True))
        sorted_chart_down = dict(sorted(self._numbers_chart.items(), key=lambda item: item[1]))

        top = list(islice(sorted_chart_top.items(), 0, self.amount_of_draw_numbers))
        down = list(islice(sorted_chart_down.items(), 0, self.amount_of_draw_numbers))

        for n_top, n_down in zip(top, down[::-1]):
            table_chart.add_row([n_top[0], n_top[1], n_down[0], n_down[1]])

        return table_chart

    def count_date(self):
        """Counts passing the time by weeks"""

        if self._current_date:
            next_date = self._current_date + timedelta(days=7) if self._draw_counter % self._draws_per_week == 0 \
                else self._current_date
        else:
            self._current_date = datetime.today()
            next_date = self._current_date

        current_week_year = datetime.date(next_date).isocalendar()
        week = current_week_year[1] if current_week_year[1] > 9 else f"0{current_week_year[1]}"
        year = current_week_year[0]

        self._current_date = next_date
        return f"{week}/{year}"

    def count_percentage(self, correct_guesses):
        """This counts percentage value of how many guess of the particular number of total draw was success"""
        return round(100 / self._draw_counter * correct_guesses, 3)

    def lottery_won(self):
        """In case of 6 numbers of 6 was guessed correctly - means lottery is won, the tossing will stop"""
        print()
        print(f"!!! {texts['won1'][self.lang]}{self._draw_counter}!!!")
        # print(f"{texts['your_was'][self.lang]} {self._defined_numbers_for_draw} {texts['drawn_was'][self.lang]} "
        # f"{self._drawn_numbers}!!!")
        print(f"{texts['won2'][self.lang]} {self.count_years()} {texts['won3'][self.lang]}")

    def count_years(self):
        """This counts the time evaluated to win"""
        return round(self._draw_counter / 52, 0)

