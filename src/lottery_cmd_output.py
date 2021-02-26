# coding=utf-8
"""LotteryCmdOutput class"""

# local library imports
from texts import texts
# external library imports
from prettytable import PrettyTable
from itertools import islice


class LotteryCmdOutput:
    """Creates statistics tables for cmd output"""

    def __init__(self, lang):
        self.lang = lang
        self.table_input = PrettyTable(header=False)
        self.table_draw = PrettyTable(header=False)
        self.table_stat = PrettyTable()
        self.table_chart = PrettyTable()

    def create_table_input(self, user_defined_numbers, random_numbers, draws_per_week):
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

    def create_table_draw(self, date, draw_counter, drawn_numbers):
        self.table_draw.add_rows([
            [
                texts['date'][self.lang].upper(),
                date
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

    def create_table_stat(self, guessed_table):
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
                    self.count_percentage(guess_num[0][0]),
                    guess_num[1][0],
                    f"#{guess_num[1][1] if guess_num[1][1] > 0 else '-'}",
                    self.count_percentage(guessed_table[key][1][0]),
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

        for n_top, n_down in zip(top, down[::-1]):
            self.table_chart.add_row([n_top[0], n_top[1], n_down[0], n_down[1]])

        return self.table_chart
