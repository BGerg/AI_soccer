from inventory import Player


class GameStates:
    """
    Játékállapot tárolás. Ilyen például, hogy kinél van a labda vagy épp bedobás van vagy kirúgás...stb
    """
    def __init__(self):
        self.ball_owner: Player = None


class GameStateSingleton:
    _states = GameStates()

    @classmethod
    def get(cls):
        return cls._states

    @classmethod
    def set_actions(cls, states: GameStates):
        cls._states = states