import heapq
import random
from dataclasses import dataclass
from typing import List, Tuple, Optional

from src.entities.area import Point


class AntMover:
    @staticmethod
    def get_neighbors(hex_q: int, hex_r: int) -> List[Tuple[int, int]]:
        """Возвращает координаты 6 соседних гексов"""
        return [
            (hex_q + 1, hex_r),  # Вправо
            (hex_q - 1, hex_r),  # Влево
            (hex_q, hex_r + 1),  # Вверх-вправо
            (hex_q, hex_r - 1),  # Вниз-влево
            (hex_q + 1, hex_r - 1),  # Вниз-вправо
            (hex_q - 1, hex_r + 1)  # Вверх-влево
        ]

    @staticmethod
    def heuristic(a: Tuple[int, int], b: Tuple[int, int]) -> float:
        """Эвристическая функция для A* (гексагональное расстояние)"""
        return (abs(a[0] - b[0]) + abs(a[0] + a[1] - b[0] - b[1]) + abs(a[1] - b[1])) / 2

    @staticmethod
    def createPath(
            start_point: Point,
            finish_point: Point,
            game_map: dict[Tuple[int, int], Point],
            max_steps: int = 3
    ) -> list[Tuple[int, int]]:
        import heapq

        start = (start_point.q, start_point.r)
        goal = (finish_point.q, finish_point.r)

        if start == goal:
            return []

        if goal not in game_map:
            return []

        frontier = []
        heapq.heappush(frontier, (0, start))

        came_from = {start: None}
        cost_so_far = {start: 0}

        while frontier:
            current = heapq.heappop(frontier)[1]

            if current == goal:
                break

            for neighbor in AntMover.get_neighbors(*current):
                if neighbor not in game_map:
                    continue

                point = game_map[neighbor]
                if point.cell_type == 5:  # Непроходимый камень
                    continue
                if point.enemy is not None:  # Враг
                    continue

                move_cost = point.cost
                new_cost = cost_so_far[current] + move_cost

                # Не продолжаем путь, если превысили лимит по шагам
                if new_cost > max_steps:
                    continue

                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + AntMover.heuristic(goal, neighbor)
                    heapq.heappush(frontier, (priority, neighbor))
                    came_from[neighbor] = current

        # Восстановление пути
        path = []
        current = goal
        while current != start:
            path.append(current)
            current = came_from.get(current, None)
            if current is None:  # Путь не найден
                return []
        path.reverse()  # Теперь путь: [step1, step2, ..., finish_point]

        # Не включаем стартовую клетку, ограничиваем по длине
        return path[:max_steps]

    @staticmethod
    def createRandomPath(start_point: Point, game_map: dict[Tuple[int, int], Point], length: int = 4, avoid_point: Point | None = None) -> List[
        Tuple[int, int]]:
        path = [(start_point.q, start_point.r)]
        current = path[0]

        for _ in range(length):
            neighbors = [n for n in AntMover.get_neighbors(*current)
                         if n in game_map and game_map[n].cell_type != 5 and game_map[n].enemy is None]

            if not neighbors:
                break

            if avoid_point:
                # Сортируем соседей по убыванию расстояния от avoid_point
                neighbors.sort(
                    key=lambda n: -((n[0] - avoid_point.q) ** 2 + (n[1] - avoid_point.r) ** 2)
                )

            next_step = random.choice(neighbors[:5]) if len(neighbors) > 1 else neighbors[0]
            path.append(next_step)
            current = next_step

        return path[1:] if len(path) > 1 else []