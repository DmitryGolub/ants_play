import heapq
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
    def createPath(start_point: Point, finish_point: Point, game_map: dict[Tuple[int, int], Point]) -> List[
            Tuple[int, int]]:
        start = (start_point.q, start_point.r)
        goal = (finish_point.q, finish_point.r)

        if start == goal:
            return [start]

        if goal not in game_map:
            return []

        frontier = []
        heapq.heappush(frontier, (0, start))

        came_from = {start: None}
        cost_so_far = {start: 0}

        while frontier:
            current = heapq.heappop(frontier)[1]

            if current == goal:
                break  # Путь найден

            for neighbor in AntMover.get_neighbors(*current):
                # Проверяем доступность соседа
                if neighbor not in game_map:
                    continue

                point = game_map[neighbor]

                # Проверяем, можно ли переместиться на эту клетку
                if point.cell_type == 5:  # Камень - непроходим
                    continue
                if point.enemy is not None:  # Клетка занята врагом
                    continue

                # Стоимость перемещения (может быть адаптирована)
                move_cost = point.cost
                new_cost = cost_so_far[current] + move_cost

                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + AntMover.heuristic(goal, neighbor)
                    heapq.heappush(frontier, (priority, neighbor))
                    came_from[neighbor] = current

        # Восстанавливаем путь (если он существует)
        path = []
        current = goal
        while current != start:
            path.append(current)
            current = came_from.get(current, None)
            if current is None:  # Путь не найден
                return []

        path.append(start)
        path.reverse()
        return path
