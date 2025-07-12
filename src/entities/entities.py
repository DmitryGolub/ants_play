from dataclasses import dataclass


@dataclass
class Food:
    q: int
    r: int
    type: int
    amount: int


@dataclass
class Ant:
    q: int
    r: int
    type: int
    health: int
    id: str
    food: Food | None = None


@dataclass
class Point:
    q: int
    r: int
    cell_type: int  # тип клетки (1-муравейник, 2-пустой, 3-грязь, 4-кислота, 5-камень)
    cost: int  # стоимость хода по клетки
    friend: Ant | None = None  # если есть друг-муравей, если нет то None
    enemy: Ant | None = None  # если есть враг-муравей, если нет то None
    food: Food | None = None  # еда если есть
    is_spot: bool = False  # является ли клетка спотом
    is_home: bool = False  # является ли клекта домом