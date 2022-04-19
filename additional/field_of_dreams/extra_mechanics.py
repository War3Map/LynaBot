from random import randint, choice, uniform
from typing import Tuple


def bank_action(current_score, add_score) -> Tuple[int, bool]:
    """
    Bankrot)

    :param current_score:
    :param add_score:
    :return: continue turn state and given score
    """
    return False, -current_score


def zero_action(current_score, add_score) -> Tuple[int, bool]:
    """

    :param score:
    :return:  score and turn over state
    """
    return True, 0


def x2_action(current_score, add_score) -> Tuple[int, bool]:
    """

    :param score:
    :return:  score and turn over state
    """
    return True, current_score * 2


def prize_action(current_score, add_score) -> Tuple[int, bool]:
    """

    :param score:
    :return:  score and turn over state
    """
    random_value = choice((5000, 0))
    return True, random_value
