# coding=utf-8

# local library imports
from lottery import Lottery
from texts import texts
from env import ver
# standard library imports
from os import system
import msvcrt
# external library import
from prettytable import PrettyTable


def main():
    """Main function"""

    """User will at first select language for the Lottery app"""
    system('cls')
    print("1. EN\n"
          "2. SK\n")

    lang_input = msvcrt.getch()
    # 0 = English, 1 = Slovak
    try:
        if int(lang_input) != 2:
            lottery = Lottery(0)
        else:
            lottery = Lottery(1)
    except ValueError:
        lottery = Lottery(0)

    system('cls')
    welcome_table(lottery.lang)
    print()
    lottery.user_inputs()

def welcome_table(lang):
    """Draving welcome table"""
    table_welcome = PrettyTable(header=False)

    table_welcome.add_rows([
        [texts['welcome1'][lang]],
        [texts['welcome2'][lang]],
        [f"{texts['welcome3'][lang]}{ver}"]
        ])

    print(table_welcome)


if __name__ == '__main__':
    main()
