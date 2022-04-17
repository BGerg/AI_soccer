from pygame import quit, K_q, K_a, QUIT, KEYDOWN
from pygame.event import get as get_pygame_event

from inventory import InventorySingleton
from game_states import GameStateSingleton, GameStates


def when_pressed(key):
    """
    Abban segít, hogy egyszerűen futtassak logikát egy billentyű nyomáshoz.
    Néha nem érzékel billentyű nyomást de a példa szempontjából ez most mind1.
    """
    def _decorator(func):
        def wrapper(self):
            for event in get_pygame_event():
                if event.type == QUIT:
                    quit()
                    exit(0)
                if event.type == KEYDOWN:
                    if event.key == key:
                        func(self)
        return wrapper
    return _decorator


class Event:
    """
    Ez az interface az összes olyan akciónak ami történhet egy meccs alatt (pl.: bedobás, passzolás, kirúgás...)
    """
    def do(self):
        pass


class Exit(Event):
    """
    Semmi keresnivalója itt de akartam szemléltetni egyszerű fügvvényben, hogy hogy kell használni az eventet itt.
    """
    @when_pressed(K_q)
    def do(self):
        quit()
        exit(0)


class Pass(Event):
    """
    Konkrét passzolós példa. Kukkold meg hogyan kérem le az objectumokat az inventorytól meg az állapot konténertől.
    """
    @when_pressed(K_a)
    def do(self):
        ball = InventorySingleton.get().ball
        ball_owner = GameStateSingleton.get().ball_owner

        pass_to = InventorySingleton.get().player_1
        if ball_owner == pass_to:
            pass_to = InventorySingleton.get().player_2

        print(f"Ball location: {ball.get_position()}, owner: {GameStateSingleton.get().ball_owner.get_player_name()}")
        print("Passing ball...")

        GameStateSingleton.get().ball_owner = pass_to
        ball.set_position(*pass_to.get_position())

        print(f"Ball location: {ball.get_position()}, owner: {GameStateSingleton.get().ball_owner.get_player_name()}")
        print("\n")


def initialize_logic():
    game_states = GameStates()
    game_states.ball_owner = InventorySingleton.get().player_1
    GameStateSingleton.set_actions(game_states)


def start_match():
    events = [Exit(), Pass()]
    while True:
        for event in events:
            event.do()

