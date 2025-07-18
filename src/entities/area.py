from typing import Optional
from src.entities.entities import Point, Food, Ant
from src.lib import write_json


class Area:
    def __init__(self):
        self.points: list[Point] = []
        self.coord_to_point: dict[tuple, Point] = {}

    def getPoint(self, q: int, r: int) -> Point | None:
        """Получить точку по координатам"""
        return self.coord_to_point.get((q, r))

    def getFood(self) -> list[Point]:
        """Получить все точки с едой"""
        return [p for p in self.points if p.food is not None]

    def getEnemies(self) -> list[Point]:
        """Получить все точки с врагами"""
        return [p for p in self.points if p.enemy is not None]

    def getSpot(self) -> Point | None:
        """Получить спот"""
        for p in self.points:
            if p.is_home:
                return p
        return None

    def getHome(self) -> list[Point]:
        """
        Возвращает список всех точек, которые являются частью дома (home).
        """
        return [p for p in self.points if p.is_home]

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
            food_obj = Food(q=ant['q'], r=ant['r'], type=f.get('type'), amount=f.get('amount')) if f and f.get("amount",
                                                                                                               0) else None
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
            food_obj = Food(q=enemy['q'], r=enemy['r'], type=f.get('type'), amount=f.get('amount')) if f and f.get("amount",
                                                                                                               0) else None
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

        write_json(response)

    def get_nearest_ant(self, point: Point, army) -> Ant | None:
        """
        Найти ближайшего своего НЕЗАНЯТОГО муравья к данной точке (Point).
        Возвращает Ant или None, если свободных муравьёв нет.
        """
        # Соберём ID всех занятых
        busy_ids = {ant.id for ant in army.busy_ants}

        min_dist = float('inf')
        nearest_ant = None
        for p in self.points:
            if p.friend and p.friend.id not in busy_ids:
                dist = self.hex_distance(point.q, point.r, p.q, p.r)
                if dist < min_dist:
                    min_dist = dist
                    nearest_ant = p.friend
        return nearest_ant

    @staticmethod
    def hex_distance(q1, r1, q2, r2):
        # Кубическая метрика для гекс-сетки (axial coords)
        return max(abs(q1 - q2), abs(r1 - r2), abs((-q1 - r1) - (-q2 - r2)))

    def detect_near_enemies(self, radius: int = 10) -> list[Ant]:
        """
        Возвращает список врагов в радиусе radius от базы (spot).
        """
        center = self.getSpot()
        if center is None:
            print("База (spot) не найдена!")
            return []

        enemies = []
        for p in self.points:
            if p.enemy:
                dist = self.hex_distance(center.q, center.r, p.q, p.r)
                if dist <= radius:
                    enemies.append(p.enemy)
        return enemies
    # remember last points, unavailable now.
    def get_nearest_food(self, ant: Ant) -> Point | None:
        min_dist = float('inf')
        nearest_food = None
        for p in self.points:
            if p.food:
                dist = self.hex_distance(ant.q, ant.r, p.q, p.r)
                if dist < min_dist:
                    min_dist = dist
                    nearest_food = p
        return nearest_food
