# coding=utf-8
"""The Lottery project"""

# standard library imports
import random
from os import system
# external library imports
from prettytable import PrettyTable


class Lottery:
    """Lottery class"""

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

    def numbers_input(self):
        """This clarifies if user want to use his own numbers or just leave it for random AI choices"""
        system('cls')
        user_input = input("Please input your 6 numbers from 1 to 49)\n"
                           "Example: 2 7 13 28 29 32 46\n"
                           "If you want every toss random numbers, just press ENTER.")

        self.specified_numbers = self.parse_and_validate_input(user_input) if user_input != "" else False
        self.decide_lottery_numbers()

    def parse_and_validate_input(self, user_input):
        """This will parse and validate user input. If the input is incorrect, back to initial question"""
        try:
            numbers = [int(element) for element in user_input.split() if int(element) in range(1, 50)]
            return numbers if len(numbers) == 6 else self.failed_validation()
        except ValueError:
            self.failed_validation()

    def failed_validation(self):
        """This prints the reason of incorrect validation and starts user input again"""
        print("Please enter numbers exactly the way specified.")
        self.numbers_input()

    def decide_lottery_numbers(self):
        """This check before lottery start if user speified numbers, if not, it picks random before every toss"""
        self.lottery_numbers = sorted(self.specified_numbers if self.specified_numbers else self.random_numbers())

        self.start_lottery()

    @staticmethod
    def random_numbers():
        """Picks 6 random numbers instead of the user"""
        return [random.randrange(1, 50) for _ in range(6)]

    def start_lottery(self):
        """This will toss lottery"""
        system('cls')
        print(f"Toss #{self.toss_counter}")
        self.drawn_numbers = sorted(self.random_numbers())

        print(f"Your lottery numbers are: {self.lottery_numbers}")
        print(f"Drawn numbers are: {self.drawn_numbers}")

        self.evaluate_round()

        if self.guessed_six != 0:
            self.lottery_won()

        # if self.toss_counter % 1000 == 0:
        self.print_results()
        self.decide_lottery_numbers()

    def evaluate_round(self):
        """This will compare user numbers against drawn numbers for the round"""
        guessed = len(set(self.lottery_numbers).intersection(self.drawn_numbers))

        if guessed == 0: self.guessed_zero += 1
        if guessed == 1: self.guessed_one += 1
        if guessed == 2: self.guessed_two += 1
        if guessed == 3: self.guessed_three += 1
        if guessed == 4: self.guessed_four += 1
        if guessed == 5: self.guessed_five += 1
        if guessed == 6: self.guessed_six += 1
        self.toss_counter += 1

    def lottery_won(self):
        """In case of 6 numbers of 6 was guessed correctly - means lottery is won, the tossing will stop"""
        system('cls')
        print(f"!!! YOU WON ON TOSS #{self.toss_counter}!!!")
        print(f"Your numbers was {self.lottery_numbers} and drawn numbers was {self.drawn_numbers}!!!")
        print(f'If you will put a lottery 1 per week, you need approximatelly {self.count_years()} to win.')

    def print_results(self):
        """This prints current result after every 1 000 toss"""
        table = PrettyTable()

        table.field_names = ["Guessed", "Times"]
        table.add_row(["0 numbers", self.guessed_zero])
        table.add_row(["1 number", self.guessed_one])
        table.add_row(["2 numbers", self.guessed_two])
        table.add_row(["3 numbers", self.guessed_three])
        table.add_row(["4 numbers", self.guessed_four])
        table.add_row(["5 numbers", self.guessed_five])
        table.add_row(["6 numbers", self.guessed_six])

        print(table)

    def count_years(self):
        """This counts the time evaluated to win"""
        return round(self.toss_counter / 52, 0)


Lottery().numbers_input()

