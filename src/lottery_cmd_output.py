# coding=utf-8
"""LotteryCmdOutput class"""

# standard imports
from itertools import islice
from datetime import datetime, timedelta
# external library imports
from prettytable import PrettyTable
# local library imports
from texts import texts

class LotteryCmdOutput:
    """Creates statistics tables for cmd output"""

    def __init__(self, lang, draws_per_week):
        self.lang = lang
        self.draws_per_week = draws_per_week
        self.table_input = PrettyTable(header=False)
        self.table_draw = PrettyTable(header=False)
        self.table_stat = PrettyTable()
        self.table_chart = PrettyTable()
        self.current_date = None

    def create_table_input(self, user_defined_numbers, random_numbers,
                           draws_per_week):
        """Method gathering inputs for table"""

        self.table_input.clear_rows()
        self.table_input.add_rows([
            [
                texts['your_nums'][self.lang].upper(),
                f"{' '.join(map(str, user_defined_numbers))}        "
            ],
            [
                texts['random_nums'][self.lang].upper(),
                ' '.join(map(str, random_numbers))
            ],
            [
                texts['draws_p_w'][self.lang].upper(),
                draws_per_week
            ],
        ])

        self.table_input.align = "l"
        return self.table_input

    def create_table_draw(self, draw_counter, drawn_numbers):
        """Method builds draw table"""
        self.table_draw.clear_rows()
        self.table_draw.add_rows([
            [
                texts['date'][self.lang].upper(),
                self.count_date(draw_counter)
            ],
            [
                texts['draw'][self.lang],
                f"{draw_counter:,}                         "
            ],
            [
                texts['drawn_nums'][self.lang].upper(),
                ' '.join(map(str, drawn_numbers))]]
        )

        self.table_draw.align = "l"
        return self.table_draw

    def count_date(self, draw_counter):
        """Counts passing the time by weeks"""

        if self.current_date:
            next_date = self.current_date + timedelta(days=7) if draw_counter\
                % self.draws_per_week == 0 else self.current_date
        else:
            current_date = datetime.today()
            next_date = current_date

        week, year = self.current_week_year(next_date)

        self.current_date = next_date
        return f"{week}/{year}"

    @staticmethod
    def current_week_year(date):
        """Count week and year based on date"""
        week_year = datetime.date(date).isocalendar()
        week = week_year[1] if week_year[1] > 9 else f"0{week_year[1]}"
        year = week_year[0]

        return week, year

    def create_table_stat(self, guessed_table, draw_counter):
        """Runs building of table"""
        self.table_stat.title = texts['tab_title_stat'][self.lang]

        self.table_stat.field_names = [texts['table_f1'][self.lang],
                                       texts['table_f2'][self.lang],
                                       texts['table_f3'][self.lang],
                                       texts['table_f4'][self.lang],
                                       texts['table_f5'][self.lang],
                                       texts['table_f6'][self.lang],
                                       texts['table_f7'][self.lang]]

        self.table_stat.align[texts['table_f1'][self.lang]] = "l"
        self.table_stat.align[texts['table_f2'][self.lang]] = "r"
        self.table_stat.align[texts['table_f3'][self.lang]] = "r"
        self.table_stat.align[texts['table_f4'][self.lang]] = "r"
        self.table_stat.align[texts['table_f5'][self.lang]] = "r"
        self.table_stat.align[texts['table_f6'][self.lang]] = "r"
        self.table_stat.align[texts['table_f7'][self.lang]] = "r"

        self.table_stat.clear_rows()
        for i, key in zip(range(len(guessed_table)), guessed_table.keys()):
            if i == 0:
                nms = 'numss'
            elif i == 1:
                nms = 'num'
            elif 1 < i < 5:
                nms = 'nums'
            else:
                nms = 'numss'

            guess_num = guessed_table[key]

            self.table_stat.add_row(
                [
                    f"{i} {texts[nms][self.lang]}",
                    guess_num[0][0],
                    f"#{guess_num[0][1] if guess_num[0][1] > 0 else '-'}",
                    self.count_percentage(draw_counter, guess_num[0][0]),
                    guess_num[1][0],
                    f"#{guess_num[1][1] if guess_num[1][1] > 0 else '-'}",
                    self.count_percentage(draw_counter,
                                          guessed_table[key][1][0]),
                ]
             )

        return self.table_stat

    @staticmethod
    def count_percentage(draw_counter, correct_guesses):
        """This counts percentage value of how many guess of the particular
         number of total draw was success"""

        return round(100 / draw_counter * correct_guesses, 3)

    def create_table_chart(self, amount_of_draw_numbers, numbers_chart):
        """Creates table chart"""

        self.table_chart.title = f"TOP {amount_of_draw_numbers}" \
                                 f"{texts['tab_title_chart'][self.lang]}"
        self.table_chart.field_names = [texts['chart_top_nm'][self.lang],
                                        texts['chart_top_val'][self.lang],
                                        texts['chart_down_nm'][self.lang],
                                        texts['chart_down_val'][self.lang]]

        self.table_chart.align[texts['chart_top_val'][self.lang]] = "r"
        self.table_chart.align[texts['chart_down_val'][self.lang]] = "r"

        sorted_chart_top = dict(sorted(numbers_chart.items(), key=lambda item:
                                item[1], reverse=True))
        sorted_chart_down = dict(sorted(numbers_chart.items(), key=lambda item:
                                        item[1]))

        top = list(islice(sorted_chart_top.items(), 0, amount_of_draw_numbers))
        down = list(islice(sorted_chart_down.items(), 0,
                           amount_of_draw_numbers))

        self.table_chart.clear_rows()
        for n_top, n_down in zip(top, down[::-1]):
            self.table_chart.add_row([n_top[0], n_top[1], n_down[0], n_down[1]])

        return self.table_chart

    def random_numbers_won(self, random_numbers_won, draw):
        """In case of win"""

        week, year = self.current_week_year(self.current_date)

        print(f"{texts['random_won1'][self.lang]} "
              f"{' '.join(map(str, random_numbers_won))} "
              f"{texts['random_won2'][self.lang]}{draw}!!!")
        print(f"{texts['random_won3'][self.lang]} {week}, "
              f"{texts['random_won4'][self.lang]} {year}.")

#
# cmd = LotteryCmdOutput(0, 2)
# cmd.current_date = datetime.today()
# cmd.random_numbers_won([1, 2, 3, 4, 5, 6], 3434)
