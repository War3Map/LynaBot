class SessionExistsError(Exception):
    def __init__(self, message="SessionExistsError: session with this name exists!"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'


class SessionNotExistsError(Exception):
    def __init__(self, message="SessionNotExistsError: session with this name not exists!"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'


class GameSessions:
    sessions = None

    def __init__(self):
        self.sessions = {}

    def __getitem__(self, key):
        return self.sessions.get(key, None)

    def add(self, session_name, game, players):
        """
        Adds new game session

        :param session_name:
        :param game:
        :param players:
        :return:
        """
        if session_name in self.sessions:
            raise SessionExistsError()
        self.sessions[session_name] = GameSession(players, session_name, game)

    def add_player(self, session_name, player_name):
        """
        Adds new owner to session

        :param player_name:
        :param session_name:
        :return:
        """
        if session_name not in self.sessions:
            raise SessionNotExistsError()
        self.sessions[session_name].session_game.add(player_name)

    def find_player(self, session_name, player_name):
        """
        Checks if player in game session
        """
        return self.sessions[session_name].in_game(player_name)

    def close(self, session_name: str):
        """
        Closes game session

        :param session_name: session name
        :return:
        """
        if session_name not in self.sessions:
            raise SessionNotExistsError()
        return self.sessions.pop(session_name)

    def exists(self, session_name):
        """
        Checks if session exists

        :param session_name: session name
        :return:
        """
        return session_name in self.sessions

    def get_game(self, session_name):
        """
        Get game for  session

        :param session_name: session name
        :return:
        """
        return self.sessions[session_name].session_game


class GameSession:
    game = None
    players = None  # Session owners
    session_name = None

    def __init__(self, players: list, session_name: str, game):
        """
        Initializess game session

        :param players: list of players (owners, of session)
        :param session_name: session unique name
        :param game: game object for play
        """

        self.game = game
        self.players = players if players is not None else []
        self.session_name = session_name

    def add(self, player_name):
        self.players.append(player_name)

    def in_game(self, player_name):
        return True if player_name in self.players else False

    @property
    def current_game(self):
        return self.game

    @property
    def session_game(self):
        return self.game
