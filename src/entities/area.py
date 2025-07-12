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

    def print_map(self):
        if not self.points:
            print("Карта пуста!")
            return

        min_q = min(p.q for p in self.points)
        max_q = max(p.q for p in self.points)
        min_r = min(p.r for p in self.points)
        max_r = max(p.r for p in self.points)

        # Символы для всего
        cell_symbols = {
            1: "🏠",  # муравейник
            2: "⬡",  # пустой
            3: "🟫",  # грязь
            4: "🧪",  # кислота
            5: "🪨",  # камни
        }
        ant_symbols = {0: "🧑‍🌾", 1: "🛡️", 2: "🦟"}  # рабочий, боец, разведчик
        enemy_symbol = "👹"
        food_symbols = {1: "🍏", 2: "🍞", 3: "🍯"}
        spot_symbol = "⭐"
        empty = "  "

        map_dict = {(p.q, p.r): p for p in self.points}

        print(f"Ход: {getattr(self, 'turnNo', '?')}  Очки: {getattr(self, 'score', '?')}\n")
        for r in range(min_r, max_r + 1):
            line = " " * ((r - min_r) % 2 * 2)
            for q in range(min_q, max_q + 1):
                point = map_dict.get((q, r))
                if not point:
                    line += empty
                    continue

                # 1. Враг
                if point.enemy:
                    hp = point.enemy.health
                    line += f"{enemy_symbol}"
                # 2. Свой муравей
                elif point.friend:
                    sym = ant_symbols.get(point.friend.type, "🐜")
                    # Можно показать HP мелко или цифрой, если надо:
                    line += f"{sym}"
                # 3. Еда
                elif point.food:
                    fs = food_symbols.get(point.food.type, "❓")
                    line += f"{fs}"
                # 4. Спот (центр муравейника)
                elif point.is_spot:
                    line += spot_symbol
                # 5. Дом
                elif point.is_home:
                    line += "🏡"
                # 6. Просто клетка
                else:
                    line += cell_symbols.get(point.cell_type, "⬡")
            print(line)

        print("\nЛегенда:")
        print("🧑‍🌾 — рабочий   🛡️ — боец   🦟 — разведчик")
        print(f"{enemy_symbol} — враг")
        print("🍏 — яблоко   🍞 — хлеб   🍯 — нектар")
        print("🏡 — гекс муравейника   ⭐ — основной гекс муравейника")
        print("🟫 — грязь   🧪 — кислота   🪨 — камень   ⬡ — пустой")

        # Подробные списки (при необходимости)
        friends = [p for p in self.points if p.friend]
        enemies = [p for p in self.points if p.enemy]
        foods = [p for p in self.points if p.food]
        if friends:
            print("\nТвои муравьи:")
            for p in friends:
                a = p.friend
                tstr = {0: "рабочий", 1: "боец", 2: "разведчик"}.get(a.type, "?")
                cargo = f", несёт: {food_symbols.get(a.food.type, '?')}{a.food.amount}" if a.food else ""
                print(f" - {tstr} @({a.q},{a.r}) HP:{a.health}{cargo}")

        if enemies:
            print("\nВраги рядом:")
            for p in enemies:
                e = p.enemy
                tstr = {0: "рабочий", 1: "боец", 2: "разведчик"}.get(e.type, "?")
                print(f" - {tstr} @({e.q},{e.r}) HP:{e.health}")

        if foods:
            print("\nРесурсы на поле:")
            for p in foods:
                f = p.food
                tstr = {1: "яблоко", 2: "хлеб", 3: "нектар"}.get(f.type, "?")
                print(f" - {tstr} @({f.q},{f.r}) x {f.amount}")

