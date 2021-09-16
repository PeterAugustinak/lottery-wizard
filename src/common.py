# coding=utf-8
"""Common functions for several modules"""

# standard library import
import random

def pick_random_numbers(lottery_pool, amount_of_draw_numbers):
    """Picks random numbers of defined amount"""
    return sorted(random.sample(range(1, lottery_pool + 1),
                                amount_of_draw_numbers))
