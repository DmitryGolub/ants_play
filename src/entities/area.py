from typing import Optional

from dataclasses import dataclass
from src.lib import getter, sender


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


class Area:
    def __init__(self):
        self.points: list[Point] = []
        self.coord_to_point: dict[tuple, Point] = {}

    def getPoint(self, q: int, r: int) -> Point | None:
        """Получить точку по координатам"""
        return self.coord_to_point.get((q, r))

    def getVegetables(self) -> list[Point]:
        """Получить все точки с едой"""
        return [p for p in self.points if p.food is not None]

    def getEnemies(self) -> list[Point]:
        """Получить все точки с врагами"""
        return [p for p in self.points if p.enemy is not None]

    def getSpot(self) -> Optional[Point]:
        """Получить спот"""
        for p in self.points:
            if p.is_spot:
                return p
        return None

    def updatePoint(self, point: Point, **kwargs):
        for key, value in kwargs.items():
            if hasattr(point, key):
                setattr(point, key, value)
            else:
                print(f"Точка не имеет поля '{key}'")

    def updateArea(self, response: dict):
        # Собираем все точки из карты
        for cell in response.get('map', []):
            q, r = cell['q'], cell['r']
            point = Point(
                q=q,
                r=r,
                cell_type=cell['type'],
                cost=cell['cost'],
            )
            self.points.append(point)
            self.coord_to_point[(q, r)] = point

        # Отмечаем home/spot
        home_coords = {(h['q'], h['r']) for h in response.get('home', [])}
        spot_coord = (response['spot']['q'], response['spot']['r']) if 'spot' in response else None
        for point in self.points:
            if (point.q, point.r) in home_coords:
                point.is_home = True
            if spot_coord and (point.q, point.r) == spot_coord:
                point.is_spot = True

        # Кладём еду
        for food in response.get('food', []):
            coord = (food['q'], food['r'])
            if coord in self.coord_to_point:
                self.coord_to_point[coord].food = Food(**food)

        # Кладём своих муравьёв
        for ant in response.get('ants', []):
            coord = (ant['q'], ant['r'])
            f = ant['food']
            food_obj = Food(**f) if f and f.get("amount", 0) else None
            ant_obj = Ant(
                q=ant['q'],
                r=ant['r'],
                type=ant['type'],
                health=ant['health'],
                id=ant['id'],
                food=food_obj
            )
            if coord in self.coord_to_point:
                self.coord_to_point[coord].friend = ant_obj

        # Кладём врагов
        for enemy in response.get('enemies', []):
            coord = (enemy['q'], enemy['r'])
            f = enemy.get('food', None)
            food_obj = Food(**f) if f and f.get("amount", 0) else None
            ant_obj = Ant(
                q=enemy['q'],
                r=enemy['r'],
                type=enemy['type'],
                health=enemy['health'],
                id=str(enemy.get('id', 'enemy')),  # если id нет - подставляем что-то своё
                food=food_obj
            )
            if coord in self.coord_to_point:
                self.coord_to_point[coord].enemy = ant_obj
