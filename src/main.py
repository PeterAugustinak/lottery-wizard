# coding=utf-8

# local library imports
from user_lottery_config import UserLotteryConfig
from lottery_engine import LotteryEngine
from texts import texts
# standard library imports
from os import system
import msvcrt
# external library import
from prettytable import PrettyTable


def main():
    """Main function"""

    lang = language_settings()

    system('cls')
    welcome_table(lang)
    print()

    user = UserLotteryConfig(lang)
    user.user_inputs()

    lottery = LotteryEngine(lang,
                            user.lottery_pool,
                            user.amount_of_draw_numbers,
                            user.lottery_numbers,
                            user.draws_per_week)

    lottery.start_lottery()

def language_settings():
    """UserLotteryConfig will at first select language for the LotteryEngine app"""
    system('cls')
    print("1. EN\n"
          "2. SK\n")

    lang_input = msvcrt.getch()
    # 0 = English, 1 = Slovak
    try:
        if int(lang_input) != 2:
            return 0
        else:
            return 1
    except ValueError:
        return 0

def welcome_table(lang):
    """Draving welcome table"""
    table_welcome = PrettyTable(header=False)

    table_welcome.add_rows([
        [texts['welcome1'][lang]],
        [texts['welcome2'][lang]],
        ])

    print(table_welcome)


if __name__ == '__main__':
    main()
