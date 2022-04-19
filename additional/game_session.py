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
        Adds new game session

        :param player_name:
        :param session_name:
        :param game:
        :param players:
        :return:
        """
        if session_name in self.sessions:
            raise SessionExistsError()
        self.sessions[session_name].session_game.add(player_name)  

    def close(self, session_name):
        """
        Closses game session
        :param session_name:
        :return:
        """
        if session_name not in self.sessions:
            raise SessionNotExistsError()
        return self.sessions.pop(session_name)

    def exists(self, session_name):
        """
        Checks if session exists

        :param session_name:
        :return:
        """
        return session_name in self.sessions

    def get_game(self, session_name):
        """
        Get game for  session

        :param session_name:
        :return:
        """
        return self.sessions[session_name].session_game


class GameSession:
    game = None
    players = None
    session_name = None

    def __init__(self, players: list, session_name: str, game):
        """
        Inits game session

        :param players: list of players
        :param session_name: session unique name
        :param game: game object for play
        """
        
        self.game = game        
        self.players = players if players is not None else []
        self.session_name = session_name
        
    def add(self, player_name):
        self.players.append(player_name)

    @property
    def session_game(self):
        return self.game
