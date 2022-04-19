from random import randint, choice, uniform
from typing import Tuple


def bank_action(current_score, add_score) -> Tuple[int, bool]:
    """

    :param score:
    :return:  score and turn over state
    """
    random_value = uniform(0.5, 1.5) * current_score
    return random_value, True


def zero_action(current_score, add_score) -> Tuple[int, bool]:
    """

    :param score:
    :return:  score and turn over state
    """
    return -current_score, True


def x2_action(current_score, add_score) -> Tuple[int, bool]:
    """

    :param score:
    :return:  score and turn over state
    """
    return current_score * 2, False


def prize_action(current_score, add_score) -> Tuple[int, bool]:
    """

    :param score:
    :return:  score and turn over state
    """
    random_value = choice((5000, 0))
    return random_value, False
