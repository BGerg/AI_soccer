from names import get_full_name


class AbstractElement:
    def __init__(self, x=0, y=0):
        self._position = (x, y)

    def set_position(self, x, y):
        self._position = (x, y)

    def get_position(self):
        return self._position


class Ball(AbstractElement): ...


class Player(AbstractElement):
    def __init__(self, x=0, y=0):
        super(Player, self).__init__(x, y)
        self._name = get_full_name()

    def get_player_name(self):
        return self._name


class Inventory:
    """
    Ez tárolja az összes objectumot ami a pályán található.
    """
    def __init__(self):
        self.ball = Ball()
        self.player_1 = Player()
        self.player_2 = Player()


class InventorySingleton:
    """
    Akárhol akarok egy elemet lekérni ettől az objectumtól biztosan le tudom kérni az inventoryt (és vele az objot).
    """
    _inventory = Inventory()

    @classmethod
    def get(cls):
        return cls._inventory if cls._inventory is not None else Inventory()

    @classmethod
    def set_instance(cls, inventory: Inventory):
        cls._inventory = inventory


def create_field():
    """
    Initialization
    """
    inventory = Inventory()

    inventory.ball = Ball(10, 20)
    inventory.player_1 = Player(10, 20)
    inventory.player_2 = Player(30, 40)

    InventorySingleton.set_instance(inventory)
