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

        validation = self.parse_and_validate_input(user_input) if user_input != "" else "aa"
        if type(validation) == list:
            print(f"Your numbers for lottery are: {[' '.join(i) for i in validation]}")
            self.specified_numbers = validation
        else:
            print(validation)
            self.numbers_input()

    @staticmethod
    def parse_and_validate_input(user_input):
        """This will parse and validate user input. If the input is incorrect, back to initial question"""
        potential_numbers = [element for element in user_input.split()]
        correct_numbers = []
        for element in potential_numbers:
            try:
                correct_numbers.append(int(element))
            except ValueError:
                return "Please input numbers the way described."
        corrected_numbers = [number for number in correct_numbers if number in range(1, 50)]
        if len(corrected_numbers) == 6:
            return corrected_numbers
        else:
            return "Please input exactly 6 numbers from 1 to 49."


    def start_lottery(self):
        pass

    def check_attempts(self):
        pass


l = Lottery()
l.numbers_input()
