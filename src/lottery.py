# coding=utf-8
"""Main class for Lottery project"""


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

    def __init__(self):
        pass

    def numbers_input(self):
        """This clarifies if user want to use his own numbers or just leave it for random AI choices"""
        user_input = input("Please input your 6 numbers from 1 to 49)\n"
                           "Example: 2 7 13 28 29 32 46\n"
                           "If you want every toss random numbers, just press ENTER.")

        self.specified_numbers = self.parse_and_validate_input(user_input) if user_input != "" else False
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
        print("Please enter numbers exactly the way specified.")
        self.numbers_input()


    def start_lottery(self):
        pass

    def random_numbers(self):
        """Picks 6 random numbers instead of the user"""

    def check_attempts(self):
        pass


l = Lottery()
l.numbers_input()
