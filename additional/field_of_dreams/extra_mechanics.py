from random import randint, choice, uniform
from typing import Tuple
import enum


class BonusTypes(enum.Enum):
    Bad = 0
    Good = 1


class TurnState(enum.Enum):
    Over = 0
    Repeat = 1


class GameBonus:
    name = "Бонуc"
    bonus_type = BonusTypes.Bad
    turn_state = TurnState.Repeat
    score = 0
    increase_score_value = 0
    message = "Это не бонус"
    score_func = lambda x: x + 100

    def __init__(self, name, type: BonusTypes,
                 message: str,
                 turn_state: TurnState,
                 increase_score_func):
        self.bonus_type = type
        self.message = message
        self.turn_state = turn_state
        self.score_func = increase_score_func
        self.can_apply = True if increase_score_func else False
        self.name = name

    def apply(self, score):
        """
        Applies bonus to score
        :param score:
        :return:
        """
        bonus_val = self.score_func(score)
        self.message = f"{self.message}. Получено {bonus_val} очков."
        return bonus_val

    # @property
    # def message(self):
    #     components = [self.message, ]
    #     if self.score_func is not None:
    #         components.append(f"Получено {} очков")


def bank_action(current_score) -> int:
    """
    Bankrot)

    :param current_score:
    :param add_score:
    :return: continue turn state and given score
    """
    return -current_score


def zero_action(current_score) -> int:
    """
    :param score:
    :return:  score and turn over state
    """
    return 0


def x2_action(current_score) -> int:
    """

    :param score:
    :return:  score and turn over state
    """
    return current_score * 2


def prize_action(current_score) -> Tuple[int, bool]:
    """

    :param score:
    :return:  score and turn over state
    """
    random_value = choice((5000, 0))
    return random_value


PRIZE = -3
PLUS = -1
X2 = -2
BANK = -4

BONUSES = {
    -4: GameBonus("Банкрот", BonusTypes.Bad, "Теперь вы банкрот!", TurnState.Over, bank_action),
    -3: GameBonus("Приз", BonusTypes.Bad, "Сектор приз на барабане!", TurnState.Repeat, prize_action),
    -2: GameBonus("Х2", BonusTypes.Bad, "Счёт удвоен!", TurnState.Repeat, x2_action),
    -1: GameBonus("Плюс", BonusTypes.Bad, "Сектор плюс на барабане!", TurnState.Repeat, None),
    0: GameBonus("Ноль", BonusTypes.Bad, "Сектор ноль!", TurnState.Repeat, None),

}
