# import codecs
# import re
import random
# import discord
from pathlib import Path

import discord
import requests

from discord.ext import commands
from additional.field_of_dreams.dream_game import DreamGame, GameStates
from additional.game_session import GameSessions, GameSession


class DreamGameCog(commands.Cog):
    """
    Entertainment bot functions
    """
    discord_bot = None
    questions_file = str(Path("additional\\field_of_dreams\\questions.csv"))
    aaaa = 3

    def __init__(self, bot):
        self.discord_bot = bot
        self.sessions = GameSessions()

    async def game_turn(self, context, game):
        """
        Game turn. Start afrer spin the drum
        :param current_player:
        :return:
        """
        current_player = game.current_player_name
        await context.send(f"Ходит игрок {current_player}\n"
                           f"Текущее слово {game.display_word}\n"
                           f"Барабан крутится за вас\n!"
                           f"Ваш счёт {game.cur_player_score}\n")

        is_player_turn, message = game.get_current_score_state()
        await context.send(f"{message}")
        if not is_player_turn:
            await self.game_turn(context, game)

    async def is_player_in_game(self, context, player_name, game):
        """
        Check if player in game
        :param context:
        :param player_name:
        :param game:
        :return:
        """
        if player_name not in game.turns_order:
            await context.send(f"Вы не в игре!")
            return False

        if player_name != game.current_player_name:
            await context.send(f"Сейчас ход игрока {game.current_player_name}!")
            return False
        return True

    async def over_turn(self, context, game, guess_result, all_in: bool = False):
        """
        Over player turn. Over game if Player wins
        :param guess_result:
        :return:
        """
        if guess_result:
            await context.send(f"Верно!")
            await context.send(f"Ваш счёт {game.cur_player_score}")
        else:
            await context.send(f"Не верно!")
            print(f"{all_in}")
            if all_in:
                await context.send(f"Игрок {game.current_player_name} проиграл")
                game.lose_player()

        if game.check_over():
            print("over")
            await context.send(game.victory_message())
        else:
            print("not over")
            await self.game_turn(context, game)

    @commands.command(description=' Запускаю поле чудес)',
                      aliases=['cg', 'start_fd', 'pole_chudes'])
    async def start_dg(self, context):
        player_name = context.message.author
        session_name = context.channel.id
        if not self.sessions.exists(session_name):
            game = DreamGame()
            game.prepare_game(question_file=DreamGameCog.questions_file)
            game.join_player(player_name)
            self.sessions.add(session_name, game, [player_name])
            await context.send(f"Внимание! Идет подготовка к игре {game.name}!")
        else:
            game: DreamGame = self.sessions.get_game(session_name)
            if game.game_state == GameStates.Running:
                await context.send(f"Игра {session_name} уже запущена!")
            elif game.game_state == GameStates.NoGame:
                game.prepare_game()
                game.join_player(player_name)
                await context.send(f"Внимание! Идет подготовка к игре {game.name}!")

    @commands.command(description='Подключаю игрока',
                      aliases=['jc', 'join_chud', 'join_dream'])
    async def join_game(self, context):
        player_name = context.message.author
        session_name = context.channel.id
        if not self.sessions.exists(session_name):
            await context.send(f"Игровая сессия {session_name} отсутствует")
            return

        game: DreamGame = self.sessions.get_game(session_name)

        if game.game_state == GameStates.Running:
            await context.send(f"Игра {session_name} уже идёт!")
            return

        print(game.turns_order)
        if player_name not in game.turns_order:
            game.join_player(player_name)
            await context.send(f"Игрок {player_name} присоеденился к {session_name}!")
        else:
            await context.send(f"Игрок {player_name} уже в игре {session_name}!")

    @commands.command(description='Запускаю поле чудес',
                      aliases=['sdg', 'start_chud', 'start_dream'])
    async def start_game(self, context):
        """
        Join player to game sessions

        :param context:
        :return:
        """
        player_name = context.message.author
        session_name = context.channel.id
        if not self.sessions.exists(session_name):
            await context.send(f"Игровая сессия {session_name} отсутствует")
            return

        game: DreamGame = self.sessions.get_game(session_name)

        if game.game_state == GameStates.Running:
            await context.send(f"Игровая сессия {session_name} уже в процессе")
            return

        start_message = game.start_game()

        await context.send(f"{start_message}!")
        await self.game_turn(context, game)

    @commands.command(description='Запускаю поле чудес',
                      aliases=['rsgd', 'restart_chud', 'restart_dream'])
    async def restart_dream_game(self, context):
        """

        :param context:
        :return:
        """
        player_name = context.message.author
        session_name = context.channel.id
        if not self.sessions.exists(session_name):
            await context.send(f" Игры {session_name} не существует!")
        else:
            game: DreamGame = self.sessions.get_game(session_name)
            if player_name not in game.players_score:
                await context.send(f"Игрок {player_name} не из игровой сессии не может перезапустить игру")
                return
            if game.game_state in (GameStates.Running, GameStates.Awaiting, GameStates.NoGame):
                await context.send(f"Игра {session_name} в процессе или ещё не создана")
            else:
                game.reload_game(question_file=DreamGameCog.questions_file)
                await self.start_game(context)

    @commands.command(description='угадай символ',
                      aliases=['guess_s', 'guess_char'])
    async def guess_symbol(self, context, symbol):
        player_name = context.message.author
        session_name = context.channel.id
        if not self.sessions.exists(session_name):
            await context.send(f"Игровая сессия {session_name} отсутствует")
            return

        if not self.sessions.exists(session_name):
            await context.send(f"Игровая сессия {session_name} отсутствует")
            return

        game: DreamGame = self.sessions.get_game(session_name)
        is_player_turn = await self.is_player_in_game(context, player_name, game)
        if not is_player_turn:
            return

        if symbol.upper() not in game.available_symbols:
            await context.send(f"Такая буква уже была."
                               f"Доступные буквы: {sorted(game.available_symbols)}")
            return

        if len(symbol) != 1:
            await context.send(f"Назовите букву, а не слово!")
            return

        guess_result = game.guess_symbol(symbol)
        await self.over_turn(context, game, guess_result)

    @commands.command(description='Покажу доступные буквы',
                      aliases=['alpha', 'show_al'])
    async def show_alpha(self, context, symbol):
        player_name = context.message.author
        session_name = context.channel.id
        if not self.sessions.exists(session_name):
            await context.send(f"Игровая сессия {session_name} отсутствует")
            return

        game: DreamGame = self.sessions.get_game(session_name)
        if not player_name in game.turns_order:
            await context.send(f"Вы не игре {session_name}!")
            return

        await context.send(f"Доступные буквы: {sorted(game.available_symbols)}")

    @commands.command(description='угадай слово',
                      aliases=['guess_w', 'guess_wor'])
    async def guess_word(self, context, word):
        player_name = context.message.author
        session_name = context.channel.id
        if not self.sessions.exists(session_name):
            await context.send(f"Игровая сессия {session_name} отсутствует")
            return

        game: DreamGame = self.sessions.get_game(session_name)
        is_player_turn = await self.is_player_in_game(context, player_name, game)
        if not is_player_turn:
            return

        if game.game_state != GameStates.Running:
            await context.send(f"Игровая сессия {session_name} не стартовала")
            return

        if len(word) == 1:
            await context.send(f"Назовите слово, а не букву!")
            return

        guess_result = game.guess_complete_word(word)
        await self.over_turn(context, game, guess_result, all_in=True)

    @commands.Cog.listener()
    async def on_message(self, message):
        pass
