import enum
import random

from dataclasses import dataclass
from random import randint
from typing import Dict, Optional, Union, List

from .game_config import DRUM_SCORES, ALPHABET
from .questions import load_questions, QUESTIONS_FILE
from .extra_mechanics import BONUSES,  TurnState, GameBonus


#
# class GameBonuses(enum.Enum):
#     Bank = BANK
#     Plus = PLUS
#     Prize = PRIZE
#     Zero = 0
#     x2 = X2


class GameStates(enum.Enum):
    NoGame = 1
    Awaiting = 2
    Running = 3
    Over = 4


# # game acrions
# STATES_ACTIONS = {
#     GameBonuses.Bank.value: bank_action,
#     GameBonuses.Zero.value: zero_action,
#     GameBonuses.x2.value: x2_action,
#     GameBonuses.Prize.value: prize_action,
#     GameBonuses.Plus.value: lambda s, ss: (True, 0)
#
# }
#

@dataclass
class DreamGame:
    """
    POLE CHUDES game!
    """
    players_score: Dict[str, int] = dict
    turns_order: List[str] = list
    game_state: Union[int, GameStates] = GameStates.Awaiting
    current_player: int = 0
    questions: Optional[Dict[str, str]] = dict
    suggested_word: str = ""
    display_word: str = ""
    symbols_remain: int = 999
    hidden_symbol: str = "-"
    victory_player: str = ""
    name: str = "Поле Чудес"
    available_symbols: List[str] = list
    all_symbols: List[str] = None
    current_score: int = 0
    turn_bonus: GameBonus = None
    current_turn: int = 0

    def change_turn(self):
        """
        Change turn to other player
        Clear all current states
        :return:
        """
        players_count = len(self.players_score)
        self.current_player = (self.current_player + 1) % players_count
        self.current_score = 0
        self.turn_bonus = None

    def __get_question_word(self):
        total_len = len(self.questions)
        random_num = randint(0, total_len - 1)
        words = [word for word in self.questions.keys()]
        return words[random_num]

    def __form_display_word(self):
        word = [self.hidden_symbol for _ in self.suggested_word]
        return "".join(word)

    def prepare_game(self, players_list: list = None, turn_order="random",
                     question_file=QUESTIONS_FILE):
        """
        Initializes game variables

        :param players_list: list of players

        :param turn_order: players orders

        :param question_file: filename with questions

        :return:
        """
        self.victory_player = ""
        self.questions = load_questions(question_file)
        self.current_player = 0
        self.game_state = GameStates.Awaiting
        if players_list is None:
            players_list = []
        self.players_score = {player: 0 for player in players_list}
        self.turns_order = players_list.copy()
        if turn_order == "random":
            random.shuffle(self.turns_order)
        self.suggested_word = self.__get_question_word()
        self.display_word = self.__form_display_word()
        self.symbols_remain = len(self.suggested_word)
        self.available_symbols = ALPHABET.copy()
        self.all_symbols = ALPHABET.copy()
        self.current_turn = 0
        self.turn_bonus = None
        # print(f"Чит {self.suggested_word}")

    def reload_game(self, turn_order="random",
                    question_file=QUESTIONS_FILE):
        """
        Reload game for second use
        :param turn_order:
        :param question_file:
        :return:
        """
        self.victory_player = ""
        self.questions = load_questions(question_file)
        self.current_player = 0
        self.game_state = GameStates.Awaiting
        players_list = self.turns_order
        if players_list is None:
            players_list = []
        self.players_score = {player: 0 for player in players_list}
        self.turns_order = players_list.copy()
        if turn_order == "random":
            random.shuffle(self.turns_order)
        self.suggested_word = self.__get_question_word()
        self.display_word = self.__form_display_word()
        self.symbols_remain = len(self.suggested_word)
        self.available_symbols = ALPHABET.copy()
        self.current_turn = 0
        self.turn_bonus = None
        # print(f"Чит {self.suggested_word}")

    def join_player(self, name):
        """
        Add player to game
        :param name:
        :return:
        """
        self.players_score[name] = 0
        self.turns_order.append(name)

    def start_game(self, order="random") -> str:
        """
        Starts a game session
        :return:
        """
        self.game_state = GameStates.Running
        question = self.questions[self.suggested_word]
        if order == "random":
            random.shuffle(self.turns_order)
        return (f"Игра началась!\n"
                f"Угадайте слово по буквам:\n"
                f"{question}"
                )

    @property
    def game_question(self) -> str:
        """
        Game_question
        :return:
        """

        return self.questions[self.suggested_word]

    @property
    def score_message(self) -> str:
        """
        Message score
        :return:
        """
        return f"{self.current_score} очков!"



    @property
    def clean_word(self) -> str:
        """
        Starts a game session
        :return:
        """
        word = [char for char in self.display_word]
        str_word = " ".join(word)
        return f"{str_word} ({len(self.display_word)})"

    def stop_game(self) -> str:
        """
        Stops game
        :return:  game over message
        """
        self.game_state = GameStates.Awaiting
        return (f"Игра окончена!\n"
                f"{self.suggested_word}"
                )

    def reset_score(self):
        """
        Reset score for current player
        :return:
        """
        player_name = self.turns_order[self.current_player]
        self.players_score[player_name] = 0

    def guess_symbol(self, guess_symbol: str):  # success_state = False
        """
        Guess separate symbol

        :param guess_symbol:
        :return:
        """

        # TODO: bad replace
        guess_symbol = guess_symbol.upper()

        count_symbols = self.suggested_word.count(guess_symbol)
        self.symbols_remain -= count_symbols

        new_display = list(self.display_word)
        for idx, symbol in enumerate(self.suggested_word):
            if guess_symbol == symbol:
                new_display[idx] = symbol

        self.display_word = "".join(new_display)

        if count_symbols > 0:
            self.increase_score()
        else:
            self.change_turn()
        self.available_symbols.remove(guess_symbol)
        return True if count_symbols > 0 else False

    def remove_current_player(self):
        """
        Removes player from game
        :return:
        """
        self.turns_order.pop(self.current_player)

    def guess_complete_word(self, word: str):
        """
        Guess all word
        :param word:
        :return:
        """
        player_name = self.current_player_name
        if word.upper() == self.suggested_word:
            self.symbols_remain = 0

        if self.symbols_remain > 0:
            self.change_turn()
        else:
            self.increase_score(mult=10)

        return (True, player_name) if self.symbols_remain == 0 else (False, player_name)

    def get_current_player_score(self):
        player_name = self.turns_order[self.current_player]
        return self.players_score[player_name]

    @property
    def cur_player_score(self):
        """
        Current Player score
        :return:
        """
        return self.get_current_player_score()

    def sector_plus_activate(self):
        """
        Activates sector plus bonus
        :return:
        """
        remain_symbols = [orig for dis, orig in zip(self.display_word, self.suggested_word) if
                          dis == self.hidden_symbol]
        unique_symbols = list(set(remain_symbols))
        # randomly choice symbol from remainings(no duplicates)
        if not remain_symbols:
            return

        plus_symbol = random.choice(unique_symbols)
        self.available_symbols.remove(plus_symbol.upper())

        new_display = list(self.display_word)
        for idx, symbol in enumerate(self.suggested_word):
            if plus_symbol == symbol:
                new_display[idx] = symbol
                self.symbols_remain -= 1

        self.display_word = "".join(new_display)

    def increase_score(self):
        cur_player = self.current_player_name
        self.players_score[cur_player] += self.current_score

    def increase_current_score(self, score):
        self.current_score += score

    @property
    def has_bonus(self):
        """"""
        return self.turn_bonus is not None

    def spin_drum(self):
        """
        Gets turn state and drum score.

        :return: true if need spin again
        """
        self.current_turn += 1
        self.turn_bonus = None
        drum_val = random.choice(DRUM_SCORES)
        # print(f"Выпало {drum_val}")
        bonus = None
        if drum_val in BONUSES:
            bonus = BONUSES[drum_val]
            self.turn_bonus = bonus

        if bonus is not None:
            if bonus.can_apply:
                self.current_score = bonus.apply(self.current_score)
                self.increase_score()
            # sector plus bonus activation
            if bonus.name == "Плюс":
                self.sector_plus_activate()

            if bonus.turn_state == TurnState.Over:
                # end player tirn
                self.change_turn()
                return False
            elif bonus.turn_state == TurnState.Repeat:
                # good bonus need to spin again
                return True
        self.current_score = drum_val
        return False

    @property
    def turn_info(self):
        clean_symbols = [sym for sym in self.display_word]
        clean_word = " ".join(clean_symbols)
        displayed_word = f"{clean_word} ({len(self.display_word)})"

        return (f"!!!!Ход {self.current_turn}!!!!\n"
                f"{self.game_question}\n"
                f"{displayed_word}\n"
                f"Ход игрока {self.current_player_name}\n"
                f"Счёт игрока {self.current_player_name}: "
                f"{self.cur_player_score}\n"
                f"Вращается барабан..."
                )

    def check_over(self):
        """
        Checks if game is over and finishes game
        :return:
        """
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
        """
        Displays turn message
        :return:
        """
        cur_player = self.turns_order[self.current_player]
        return f"Сейчас ход {cur_player}.."

    def lose_player(self, player_name):
        """
        Makes current player lose
        :return:
        """
        self.turns_order.remove(player_name)

    @property
    def current_player_name(self):
        """
        Gets current player name
        :return:
        """
        return self.turns_order[self.current_player]

    def victory_message(self):
        """
        Returns victory message
        :return:
        """
        other_scores = [f"{player} - {score}\n" for player, score in self.players_score.items()]
        str_scores = "\n".join(other_scores)
        win_message = (f"И перед нами победитель: {self.victory_player} !!!\n"
                       f"Весь счёт: {str_scores}")
        draw_message = (f"У нас ничья! Загаданное слово {self.suggested_word}\n !"
                        f"Весь счёт: {str_scores}")

        return (win_message
                if len(self.turns_order) != 0
                else draw_message)
