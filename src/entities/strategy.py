from plotly.graph_objs.indicator import Number

from src.entities.area import Area
from src.entities.ant import AntMover
from src.entities.army import Army
from src.entities.entities import Point


class Strategy:
    def update_state(self, army: Army, area: Area):
        self.army = army
        self.area = area

    def generate_actions(self):
        print('generationg actions:')
        a = self._generate_def_actions()
        b = self._generate_food_actions()
        c = self._generate_attack_actions()
        d = self._generate_idle_actions()
        e = self._generate_random_actions()
        res = {}
        res['moves'] = a + b + c + d + e
        return res

    def _generate_def_actions(self):
        if self.check_def():
            return self.def_orechnik()
        return []

    def _generate_random_actions(self):
        result = []
        for ant in self.army.all_ants:
            if ant.food.amount >= 5:
                print('create path')
                path = AntMover.createPath(self.area.getPoint(ant.q, ant.r), self.area.getSpot(), self.area.coord_to_point)
                result.append({
                    "ant": ant.id,
                    "path": [{"q": step[0], "r": step[1]} for step in path]
                })
            else:
                print('go random')
                start_point = self.area.coord_to_point.get((ant.q, ant.r))
                if not start_point:
                    continue

                path = AntMover.createRandomPath(start_point, self.area.coord_to_point)
                if not path:
                    continue

                result.append({
                    "ant": ant.id,
                    "path": [{"q": step[0], "r": step[1]} for step in path]
                })
        return result

    def _generate_food_actions(self):
        result = []

        for food in self.area.getFood():
            # Пропускаем, если еда уже в списке целей
            if (food.q, food.r) in self.army.busy_targets:
                continue

            # Ищем ближайшего незанятого муравья
            ant = self.area.get_nearest_ant(self.area.getPoint(food.q, food.r), self.army)
            if not ant:
                continue

            path = AntMover.createPath(
                self.area.getPoint(ant.q, ant.r),
                self.area.getPoint(food.q, food.r),
                self.area.coord_to_point
            )
            if not path:
                continue

            result.append({
                "ant": ant.id,
                "path": [{"q": step[0], "r": step[1]} for step in path]
            })

            # Отмечаем муравья и цель как занятые
            self.army.busy_ants.append(ant)
            self.army.busy_targets.append((food.q, food.r))
        return result

    def _generate_attack_actions(self):
        return []

    def _generate_idle_actions(self):
        return []

    def nearest_food_ant(self):
        pass

    def send_ant(self):
        return AntMover.createPath(self.area.coord_to_point)

    def def_orechnik(self):
        pass

    def check_def(self):
        # check nearest zone
        return False
