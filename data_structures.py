from enum import Enum

# vector 2
class V2:
    def __init__(self, q=0, r=0):
        self.q = q
        self.r = r

# ant's move. consists of multiple hexes
class Move:
    def __init__(self, ant: str = 'banana', path: list[V2] = list()):
        self.ant: str = ant
        self.path: list[V2] = path


class FoodType(Enum):
    NONE   = 0
    APPLE  = 1
    BREAD  = 2
    POLLEN = 3


class AntType(Enum):
    NONE    = -1
    WORKER  = 0
    FIGHTER = 1
    SCOUT   = 2


class HexType(Enum):
    NONE    = 0
    ANTHILL = 1
    EMPTY   = 2
    MUD     = 3
    ACID    = 4
    STONE   = 5


class Food:
    def __init__(self, amount: int = 0, kind: int | FoodType = FoodType.NONE, q: int = 0, r: int = 0):
        self.amount = amount
        self.kind = FoodType(kind)
        self.q = q
        self.r = r


class Ant:
    def __init__(
        self,
        id: str,
        food: Food = Food(),
        health: int = 100,
        last_attack: V2 = V2(),
        last_enemy_ant: str = '',
        last_move: list[V2] = list(),
        move: list[V2] = list(),
        q: int = 0,
        r: int = 0,
        kind: AntType = AntType.NONE # not valid
    ):
        self.id: str = id
        self.food = food
        self.health = health
        self.last_attack = last_attack
        self.last_enemy_ant = last_enemy_ant
        self.last_move: list[V2] = list()
        self.move = move
        self.q = q
        self.r = r
        self.kind = kind

        if self.kind == AntType.WORKER:
            self.attack = 30
            self.max_food = 8
            self.speed = 5
        elif self.kind == AntType.SCOUT:
            self.attack = 20
            self.max_food = 2
            self.speed = 7
        elif self.kind == AntType.FIGHTER:
            self.attack = 70
            self.max_food = 2
            self.speed = 4


class Hex:
    def __init__(self, q: int = 0, r: int = 0, kind: HexType = HexType.EMPTY, cost: int = 1):
        self.q = q
        self.r = r
        self.kind = kind
        self.cost = cost


if __name__ == '__main__':
    ant1 = Ant('banana')
    print(ant1.food.kind)

