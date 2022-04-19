import enum
import random

from dataclasses import dataclass
from random import randint
from typing import Dict, Optional, Union, List

from .game_config import DRUM_SCORES, BANK, PLUS, PRIZE, X2, STATES_DESCRIPTIONS, ALPHABET
from .questions import load_questions, QUESTIONS_FILE
from .extra_mechanics import x2_action, bank_action, zero_action, prize_action


class GameBonuses(enum.Enum):
    Bank = BANK
    Plus = PLUS
    Prize = PRIZE
    Zero = 0
    x2 = X2


class GameStates(enum.Enum):
    NoGame = 1
    Awaiting = 2
    Running = 3
    Over = 4


STATES_ACTIONS = {
    GameBonuses.Bank: bank_action,
    GameBonuses.Zero: zero_action,
    GameBonuses.x2: x2_action,
    GameBonuses.Prize: prize_action,
    GameBonuses.Plus: lambda s: (0, False)

}


@dataclass
class DreamGame:
    players_score: Dict[str, int] = dict
    turns_order: List[str] = list
    game_state: Union[int, GameStates] = GameStates.Awaiting
    current_player: int = 0
    questions: Optional[Dict[str, str]] = dict
    suggested_word: str = ""
    display_word: str = ""
    symbols_remain: int = 999
    hidden_symbol: str = "-"
    current_score: int = 0
    victory_player: str = ""
    name: str = "Поле Чудес"
    available_symbols: List[str] = list

    def change_turn(self):
        players_count = len(self.players_score)
        self.current_player = (self.current_player + 1) % players_count

    def __get_question_word(self):
        total_len = len(self.questions)
        random_num = randint(0, total_len)
        words = [word for word in self.questions.keys()]
        return words[random_num]

    def __form_display_word(self):
        word = [self.hidden_symbol for _ in self.suggested_word]
        return "".join(word)

    def prepare_game(self, players_list: list = None, turn_order="random",
                     question_file=QUESTIONS_FILE):
        self.victory_player = ""
        self.questions = load_questions(question_file)
        self.current_player = 0
        self.game_state = GameStates.Awaiting
        if players_list is None:
            players_list = []
        self.players_score = {player: 0 for player in players_list}
        if turn_order == "random":
            random.shuffle(players_list)
        self.turns_order = players_list.copy()
        self.suggested_word = self.__get_question_word()
        self.display_word = self.__form_display_word()
        self.symbols_remain = len(self.suggested_word)
        self.available_symbols = ALPHABET
        print(f"Чит {self.suggested_word}")

    def reload_game(self, turn_order="random",
                    question_file=QUESTIONS_FILE):
        self.victory_player = ""
        self.questions = load_questions(question_file)
        self.current_player = 0
        self.game_state = GameStates.Awaiting
        players_list = self.turns_order
        if players_list is None:
            players_list = []
        self.players_score = {player: 0 for player in players_list}
        if turn_order == "random":
            random.shuffle(players_list)
        self.turns_order = players_list.copy()
        self.suggested_word = self.__get_question_word()
        self.display_word = self.__form_display_word()
        self.symbols_remain = len(self.suggested_word)
        self.available_symbols = ALPHABET
        print(f"Чит {self.suggested_word}")

    def join_player(self, name):
        self.players_score[name] = 0
        self.turns_order.append(name)

    def start_game(self) -> str:
        self.game_state = GameStates.Running
        question = self.questions[self.suggested_word]
        return (f"Игра началась!\n"
                f"Угадайте слово по буквам:\n"
                f"{question}"
                )

    def reset_score(self):
        player_name = self.turns_order[self.current_player]
        self.players_score[player_name] = 0
        print(f"{player_name} теряет все свои очки!")

    def increase_score(self, mult=1):
        player_name = self.turns_order[self.current_player]
        increased_value = self.current_score * mult
        self.players_score[player_name] += increased_value
        print(f"{player_name} получает {increased_value}")

    def guess_symbol(self, guess_symbol: str):  # success_state = False
        # TODO: bad replace
        guess_symbol = guess_symbol.upper()

        count_symbols = self.suggested_word.count(guess_symbol)
        self.symbols_remain -= count_symbols

        new_display = list(self.display_word)
        for idx, symbol in enumerate(self.suggested_word):
            if guess_symbol == symbol:
                new_display[idx] = symbol

        self.display_word = "".join(new_display)
        # for symbol in self.suggested_word:
        #     if guess_symbol == symbol:
        #         success_state = True
        #         self.symbols_remain -= 1
        # new_display = [guess_symbol
        #                if guess_symbol == symbol
        #                else self.hidden_symbol
        #                for symbol in self.suggested_word]

        if count_symbols > 0:
            self.increase_score()
        else:
            self.change_turn()
        self.available_symbols.remove(guess_symbol)
        return True if count_symbols > 0 else False

    def remove_current_player(self):

        self.turns_order.pop(self.current_player)

    def guess_complete_word(self, word: str):  # success_state = False
        if word.upper() == self.suggested_word:
            self.symbols_remain = 0

        if self.symbols_remain > 0:
            self.change_turn()
        else:
            self.increase_score(mult=10)

        return True if self.symbols_remain == 0 else False

    def get_current_player_score(self):
        player_name = self.turns_order[self.current_player]
        return self.players_score[player_name]

    @property
    def cur_player_score(self):
        return self.get_current_player_score()

    def get_current_score_state(self):
        self.current_score = random.choice(DRUM_SCORES)
        if self.current_score not in STATES_ACTIONS:
            self.current_score = self.current_score
            return True, f"{self.current_score} очков!"

        extra_val = self.current_score
        player_score = self.get_current_player_score()
        end_turn, self.current_score = STATES_ACTIONS[self.current_score](player_score,
                                                                          extra_val)
        return end_turn, STATES_DESCRIPTIONS[extra_val]

        #

    # def word(self):
    #     return self.display_word
    def is_over(self):
        self.victory_player = self.turns_order[self.current_player]
        return True if self.symbols_remain == 0 else False

    def check_over(self):
        print(self.symbols_remain)
        if self.symbols_remain == 0:
            self.victory_player = self.turns_order[self.current_player]
            self.game_state = GameStates.Over
            return True
        elif len(self.turns_order) == 0:
            self.victory_player = ""
            self.game_state = GameStates.Over
            return True

        return False

    def display_player_message(self):
        cur_player = self.turns_order[self.current_player]
        return f"Сейчас ход {cur_player}.."

    def lose_player(self):
        """
        Makes current player lose
        :return:
        """
        self.turns_order.remove(self.current_player_name)

    @property
    def current_player_name(self):
        return self.turns_order[self.current_player]

    def victory_message(self):

        return (f"И перед нами победитель: {self.victory_player} !!!"
                if len(self.turns_order) != 0
                else "У нас ничья!")
