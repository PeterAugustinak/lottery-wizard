# coding=utf-8
"""LotteryCmdOutput class"""

# local library imports
from texts import texts
# external library imports
from prettytable import PrettyTable
from itertools import islice
from datetime import datetime, timedelta


class LotteryCmdOutput:
    """Creates statistics tables for cmd output"""

    def __init__(self, lang, draws_per_week):
        self.lang = lang
        self.draws_per_week = draws_per_week
        self.table_input = PrettyTable(header=False)
        self.table_draw = PrettyTable(header=False)
        self.table_stat = PrettyTable()
        self.table_chart = PrettyTable()
        self._current_date = None

    def create_table_input(self, user_defined_numbers, random_numbers, draws_per_week):
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

        if self._current_date:
            next_date = self._current_date + timedelta(days=7) if draw_counter % self.draws_per_week == 0 \
                else self._current_date
        else:
            current_date = datetime.today()
            next_date = current_date

        current_week_year = datetime.date(next_date).isocalendar()
        week = current_week_year[1] if current_week_year[1] > 9 else f"0{current_week_year[1]}"
        year = current_week_year[0]

        self._current_date = next_date
        return f"{week}/{year}"

    def create_table_stat(self, guessed_table, draw_counter):
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
                nm = 'num'
            elif i == 1:
                nm = 'nums'
            else:
                nm = 'numss'

            guess_num = guessed_table[key]

            self.table_stat.add_row(
                [
                    f"{i} {texts[nm][self.lang]}",
                    guess_num[0][0],
                    f"#{guess_num[0][1] if guess_num[0][1] > 0 else '-'}",
                    self.count_percentage(draw_counter, guess_num[0][0]),
                    guess_num[1][0],
                    f"#{guess_num[1][1] if guess_num[1][1] > 0 else '-'}",
                    self.count_percentage(draw_counter, guessed_table[key][1][0]),
                ]
             )

        return self.table_stat

    @staticmethod
    def count_percentage(draw_counter, correct_guesses):
        """This counts percentage value of how many guess of the particular number of total draw was success"""
        return round(100 / draw_counter * correct_guesses, 3)

    def create_table_chart(self, amount_of_draw_numbers, numbers_chart):
        self.table_chart.title = f"TOP {amount_of_draw_numbers}{texts['tab_title_chart'][self.lang]}"
        self.table_chart.field_names = [texts['chart_top_nm'][self.lang],
                                        texts['chart_top_val'][self.lang],
                                        texts['chart_down_nm'][self.lang],
                                        texts['chart_down_val'][self.lang]]

        self.table_chart.align[texts['chart_top_val'][self.lang]] = "r"
        self.table_chart.align[texts['chart_down_val'][self.lang]] = "r"

        sorted_chart_top = dict(sorted(numbers_chart.items(), key=lambda item: item[1], reverse=True))
        sorted_chart_down = dict(sorted(numbers_chart.items(), key=lambda item: item[1]))

        top = list(islice(sorted_chart_top.items(), 0, amount_of_draw_numbers))
        down = list(islice(sorted_chart_down.items(), 0, amount_of_draw_numbers))

        self.table_chart.clear_rows()
        for n_top, n_down in zip(top, down[::-1]):
            self.table_chart.add_row([n_top[0], n_top[1], n_down[0], n_down[1]])

        return self.table_chart
