# coding=utf-8
"""The Lottery project"""

# local library import
from texts import texts
# standard library imports
import random
from os import system
# external library imports
from prettytable import PrettyTable


class Lottery:
    """Lottery class"""
    lang = None
    # if user does not want to specify own numbers, every toss the random number will be set
    specified_numbers = False
    # current numbers
    lottery_numbers = None
    drawn_numbers = None
    # after every toss, it will be evaluated how many numbers user guessed correctly
    guessed_zero = 0
    guessed_one = 0
    guessed_two = 0
    guessed_three = 0
    guessed_four = 0
    guessed_five = 0
    guessed_six = 0
    # counter of lottery tosses
    toss_counter = 1

    def __init__(self):
        pass

    # USER INPUT BEFORE LOTTERY CAN START ###
    def language_input(self):
        """User will at first select language for the Lottery app"""
        system('cls')
        lang_input = input("1. ENG\n"
                           "2. SVK\n")

        if lang_input == "2":
            self.lang = 1
        else:
            self.lang = 0

        self.numbers_input()

    def numbers_input(self):
        """This clarifies if user want to use his own numbers or just leave it for random AI choices"""
        system('cls')
        user_input = input(f"{texts['intro1'][self.lang]}\n{texts['intro2'][self.lang]}\n{texts['intro3'][self.lang]}")

        self.specified_numbers = self.parse_and_validate_input(user_input) if user_input != "" else False
        self.decide_lottery_numbers()
        self.start_lottery()

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
        self.numbers_input()

    # START OF LOTTERY DRAWINGS ... ###
    def start_lottery(self):
        """This will toss lottery"""
        system('cls')
        while self.guessed_six == 0:
            self.decide_lottery_numbers()
            self.drawn_numbers = sorted(self.random_numbers())
            self.evaluate_round()

            # if self.toss_counter % 1000 == 0:
            self.print_results()

        self.lottery_won()

    def decide_lottery_numbers(self):
        """This check before lottery start if user speified numbers, if not, it picks random before every draw"""
        self.lottery_numbers = sorted(self.specified_numbers if self.specified_numbers else self.random_numbers())

    @staticmethod
    def random_numbers():
        """Picks 6 random numbers instead of the user"""
        return [random.randrange(1, 50) for _ in range(6)]

    def evaluate_round(self):
        """This will compare user numbers against drawn numbers for the dra"""
        guessed = len(set(self.lottery_numbers).intersection(self.drawn_numbers))

        if guessed == 0: self.guessed_zero += 1
        if guessed == 1: self.guessed_one += 1
        if guessed == 2: self.guessed_two += 1
        if guessed == 3: self.guessed_three += 1
        if guessed == 4: self.guessed_four += 1
        if guessed == 5: self.guessed_five += 1
        if guessed == 6: self.guessed_six += 1
        self.toss_counter += 1

    def print_results(self):
        """This prints current result after every 1 000 toss"""
        table = PrettyTable()

        table.field_names = [texts['table_f1'][self.lang], texts['table_f2'][self.lang], texts['table_f3'][self.lang]]
        table.align[texts['table_f1'][self.lang]] = "l"
        table.align[texts['table_f2'][self.lang]] = "r"
        table.align[texts['table_f3'][self.lang]] = "r"
        table.add_row([f"0 {texts['num'][self.lang]}", self.guessed_zero, self.count_percentage(self.guessed_zero)])
        table.add_row([f"1 {texts['nums'][self.lang]}", self.guessed_one, self.count_percentage(self.guessed_one)])
        table.add_row([f"2 {texts['numss'][self.lang]}", self.guessed_two, self.count_percentage(self.guessed_two)])
        table.add_row([f"3 {texts['numss'][self.lang]}", self.guessed_three, self.count_percentage(self.guessed_three)])
        table.add_row([f"4 {texts['numss'][self.lang]}", self.guessed_four, self.count_percentage(self.guessed_four)])
        table.add_row([f"5 {texts['numss'][self.lang]}", self.guessed_five, self.count_percentage(self.guessed_five)])
        table.add_row([f"6 {texts['numss'][self.lang]}", self.guessed_six, self.count_percentage(self.guessed_six)])

        system('cls')
        print(f"{texts['draw'][self.lang]}{self.toss_counter}")
        print(f"{texts['your_nums'][self.lang]}{self.lottery_numbers}")
        print(f"{texts['drawn_nums'][self.lang]}{self.drawn_numbers}")
        print(table, end='\r')

    def count_years(self):
        """This counts the time evaluated to win"""
        return round(self.toss_counter / 52, 0)

    def count_percentage(self, correct_guesses):
        """This counts percentage value of how many guess of the particular number of total draw was success"""
        return round(100 / self.toss_counter * correct_guesses, 2)

    def lottery_won(self):
        """In case of 6 numbers of 6 was guessed correctly - means lottery is won, the tossing will stop"""
        print()
        print(f"!!! {texts['won1'][self.lang]}{self.toss_counter}!!!")
        print(f"{texts['your_was'][self.lang]} {self.lottery_numbers} {texts['drawn_was'][self.lang]} "
              f"{self.drawn_numbers}!!!")
        print(f"{texts['won2'][self.lang]} {self.count_years()} {texts['won3'][self.lang]}")


Lottery().language_input()
