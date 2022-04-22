from pathlib import Path

from discord.ext import commands
from additional.field_of_dreams.dream_game import DreamGame, GameStates
from additional.game_session import GameSessions

from additional.config_loader import get_setting

RULES = "\n".join(get_setting("POLE_CHUDES_RULES"))


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

    async def check_session(self, session_name, context):
        """
        Checks if session exists

        :param session_name:
        :param context:
        :return:
        """
        if not self.sessions.exists(session_name):
            await context.send(f"Игровая сессия {session_name} отсутствует")
            return False
        return True

    async def game_turn(self, context, game):
        """
        Game turn. Start afrer spin the drum

        """
        await context.send(game.turn_info)
        repeat_spin = game.spin_drum()

        if game.has_bonus:
            additional = ""
            messages = [game.turn_bonus.current_message]
            if game.turn_bonus.name == "Плюс":
                messages.append(game.clean_word)
            await context.send("\n".join(messages))

        else:
            await context.send(game.score_message)

        if game.check_over():
            await context.send(game.victory_message())
        elif repeat_spin:
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

    async def over_turn(self, context, game, guess_result, allin_player: str = ""):
        """
        Over player turn. Over game if Player wins
        :param allin_player:
        :param guess_result:
        :return:
        """
        if guess_result:
            await context.send(f"Верно!")
        else:
            await context.send(f"Нет! Не верно!")
            # print(f"{allin_player}")
            if allin_player:
                await context.send(f"Игрок {allin_player} проиграл!")
                game.lose_player(allin_player)

        if game.check_over():
            await context.send(game.victory_message())
        else:
            await self.game_turn(context, game)

    @commands.command(description=' Запускаю поле чудес)',
                      aliases=['cg', 'start_fd', 'pole_chudes'])
    async def start_dg(self, context):
        """
        Starts the game session

        :param context:
        :return:
        """
        player_name = str(context.message.author)
        session_name = context.channel.id
        if not self.sessions.exists(session_name):
            game = DreamGame()
            game.prepare_game(question_file=DreamGameCog.questions_file)
            game.join_player(player_name)
            self.sessions.add(session_name, game, [player_name])
            await context.send(f"Внимание! Идет подготовка к игре {game.name}!\n"
                               f"Игроки могут присоедениться написав команду jc")
        else:
            game: DreamGame = self.sessions.get_game(session_name)
            if game.game_state == GameStates.Running:
                await context.send(f"Игра {session_name} уже запущена!")
            elif game.game_state == GameStates.Awaiting:
                await context.send(f"Игра {session_name} ожидает игроков")
            elif game.game_state == GameStates.NoGame:
                game.prepare_game()
                game.join_player(player_name)
                await context.send(f"Внимание! Идет подготовка к игре {game.name}!")

    @commands.command(description=' останавливаю поле чудес)',
                      aliases=['stop_fd', 'stop_pole'])
    async def stop_dg(self, context):
        """
        Stops game session

        :param context:
        :return:
        """
        player_name = str(context.message.author)
        session_name = context.channel.id
        if not self.sessions.exists(session_name):
            await context.send(f"Игровая сессия ещё не начата!")
        else:
            if not self.sessions.find_player(session_name, player_name):
                await context.send(f"Игрок {player_name} не является создателем сессии!")
                return

            self.sessions.close(session_name)
            await context.send(f"Игровая сессия {session_name} окончена!")

    @commands.command(description='Подключаю игрока',
                      aliases=['jc', 'join_chud', 'join_dream'])
    async def join_game(self, context):
        """
        Join player to game to
        :param context:
        :return:
        """
        player_name = str(context.message.author)
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

    @commands.command(description='Отключаю игрока',
                      aliases=['dc', 'exit_chud', 'exit_dream'])
    async def exit_game(self, context):
        """
        Exit player from game
        :param context:
        :return:
        """
        player_name = str(context.message.author)
        session_name = context.channel.id
        if not self.sessions.exists(session_name):
            await context.send(f"Игровая сессия {session_name} отсутствует")
            return

        game: DreamGame = self.sessions.get_game(session_name)
        if player_name in game.turns_order:
            game.leave_player(player_name)
            await context.send(f"Игрок {player_name} вышел из игры {session_name}!")

    @commands.command(description='список ироков',
                      aliases=['dream_players'])
    async def players(self, context):
        """
        Exit player from game
        :param context:
        :return:
        """
        player_name = str(context.message.author)
        session_name = context.channel.id
        if not await self.check_session(session_name, context):
            return

        game: DreamGame = self.sessions.get_game(session_name)
        current_players = "\n".join(game.turns_order)
        all_players = "\n".join(list(game.players_score))
        await context.send(f"Текущие игроки: {current_players}\nВсе игроки: {all_players}")

    @commands.command(description='Запускаю поле чудес',
                      aliases=['sdg', 'start_chud', 'start_dream'])
    async def start_game(self, context):
        """
        Starts game

        :param context:
        :return:
        """
        player_name = str(context.message.author)
        session_name = context.channel.id
        if not self.sessions.exists(session_name):
            await context.send(f"Игровая сессия {session_name} отсутствует")
            return

        if not self.sessions.find_player(session_name, player_name):
            owners = self.sessions[session_name].players
            await context.send(f"Игрок {player_name} "
                               f"не в списке {owners} "
                               f"владельцев сессии!")
            return

        game: DreamGame = self.sessions.get_game(session_name)

        if game.game_state == GameStates.Running:
            await context.send(f"Игровая сессия {session_name} уже в процессе")
            return

        start_message = game.start_game()

        await self.game_turn(context, game)

    @commands.command(description='Останавливаю игру',
                      aliases=['ssg', 'stop_chud', 'stop_dream'])
    async def stop_game(self, context):
        """
        Stops a game

        :param context:
        :return:
        """
        player_name = str(context.message.author)
        session_name = context.channel.id

        if not self.sessions.exists(session_name):
            await context.send(f"Игровая сессия {session_name} отсутствует")
            return

        if not self.sessions.find_player(session_name, player_name):
            owners = self.sessions[session_name].players
            await context.send(f"Игрок {player_name} "
                               f"не в списке {owners} "
                               f"владельцев сессии!")
            return
        game = self.sessions.get_game(session_name)
        if game.game_state == GameStates.Awaiting:
            await context.send(f"Игра в сессии {session_name} ещё не стартовала")
            return

        stop_message = game.stop_game(new_questions_file=DreamGameCog.questions_file)
        await context.send(f"Игра остановлена! {stop_message}\n"
                           f"Игроки могут присоедениться!")

    @commands.command(description='Запускаю поле чудес',
                      aliases=['rsgd', 'restart_chud', 'restart_dream'])
    async def restart_dream_game(self, context):
        """
        Restart game. Initially start new game

        :param context:
        :return:
        """
        player_name = str(context.message.author)
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
                      aliases=['guess_s', 'guess_char', 'symbol', 'sym'])
    async def guess_symbol(self, context, symbol):
        player_name = str(context.message.author)
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

        if len(symbol) != 1:
            await context.send(f"Назовите одну букву, а не слово!")
            return

        if symbol.upper() not in game.all_symbols:
            await context.send(f"Таких букв нет в алфавите."
                               f"Доступные буквы: {sorted(game.available_symbols)}")
            return

        if symbol.upper() not in game.available_symbols:
            await context.send(f"Такая буква уже была."
                               f"Доступные буквы: {sorted(game.available_symbols)}")
            return

        guess_result = game.guess_symbol(symbol)
        await self.over_turn(context, game, guess_result)

    @commands.command(description='Покажу доступные буквы',
                      aliases=['alpha', 'show_al'])
    async def show_alpha(self, context):
        """
        Shows remaining alphabet symbols
        """
        player_name = str(context.message.author)
        session_name = context.channel.id
        session_exists = await self.check_session(session_name, context)
        if not session_exists:
            return

        game: DreamGame = self.sessions.get_game(session_name)
        if player_name not in game.turns_order:
            await context.send(f"Вы не игре {session_name}!")
            return

        if player_name != game.current_player_name:
            await context.send(f"Сейчас не ваш ход!!")
            return

        await context.send(f"Доступные буквы: {sorted(game.available_symbols)}")

    @commands.command(description='Покажу доступные буквы',
                      aliases=['rules', 'dream_rules'])
    async def show_rules(self, context):
        """
        Shows rules of game
        """

        await context.send(f"{RULES}")

    @commands.command(description='угадай слово',
                      aliases=['guess_w', 'guess_wor', 'wor', 'word'])
    async def guess_word(self, context, word):
        player_name = str(context.message.author)
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

        guess_result, player_name = game.guess_complete_word(word)
        await self.over_turn(context, game, guess_result, allin_player=player_name)

    @commands.Cog.listener()
    async def on_message(self, message):
        pass
