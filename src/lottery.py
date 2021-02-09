# coding=utf-8
"""The Lottery project"""

# standard library imports
import random
from os import system

class Lottery:
    """Lottery class"""

    # if user does not want to specify own numbers, every toss the random number will be set
    specified_numbers = False
    # after every toss, it will be evaluated how many numbers user guessed correctly
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
        lottery_numbers = sorted(self.specified_numbers if self.specified_numbers else self.random_numbers())
        system('cls')

        self.start_lottery(lottery_numbers)

    @staticmethod
    def random_numbers():
        """Picks 6 random numbers instead of the user"""
        return [random.randrange(1, 50) for _ in range(6)]

    def start_lottery(self, lottery_numbers):
        """This will toss lottery"""
        print(f"Toss #{self.toss_counter}")
        tossed_numbers = sorted(self.random_numbers())

        print(f"Your lottery numbers are: {lottery_numbers}")
        print(f"Tossed numbers are: {tossed_numbers}")

        self.evaluate_round(lottery_numbers, tossed_numbers)
        self.toss_counter += 1
        self.decide_lottery_numbers()

    def evaluate_round(self, lottery_numbers, tossed_nubers):
        """This will compare user numbers against tossed numbers for the round"""
        pass



l = Lottery()
l.numbers_input()
