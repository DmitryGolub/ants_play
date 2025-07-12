from fontTools.varLib.builder import buildVarRegionAxis
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
        e = self._generate_random_actions()
        res = {}
        res['moves'] = e
        return res

    def _generate_def_actions(self):
        if self.check_def():
            return self.def_orechnik()
        return []

    # def _generate_random_actions(self):
    #     result = []
    #     no0 = []
    #     no1 = []
    #     no2 = []
    #     for ant in self.army.all_ants:
    #         if ant.food.amount >= 1:
    #             print('create path')
    #             mx = 0
    #             if ant.type == 2:
    #                 mx = 7
    #             if ant.type == 1:
    #                 mx = 4
    #             if ant.type == 0:
    #                 mx = 5
    #             path = AntMover.createPath(self.area.getPoint(ant.q, ant.r), self.area.getSpot(),
    #                                            self.area.coord_to_point, mx)
    #
    #         elif ant.type == 2:
    #             start_point = self.area.coord_to_point.get((ant.q, ant.r))
    #             if not start_point:
    #                 continue
    #             for i in range(30):
    #                 path = AntMover.createRandomPath(start_point, self.area.coord_to_point, 7)
    #                 if path and path[-1] not in no2:
    #                     no2.append(path[-1])
    #                     break
    #                 path = None
    #
    #         elif ant.type == 1:
    #             start_point = self.area.coord_to_point.get((ant.q, ant.r))
    #             if not start_point:
    #                 continue
    #             for i in range(30):
    #                 path = AntMover.createRandomPath(start_point, self.area.coord_to_point, 4)
    #                 if path and path[-1] not in no1:
    #                     no1.append(path[-1])
    #                     break
    #                 path = None
    #
    #         elif ant.type == 0:
    #             print('go random')
    #             start_point = self.area.coord_to_point.get((ant.q, ant.r))
    #             if not start_point:
    #                 continue
    #             for i in range(30):
    #                 path = AntMover.createRandomPath(start_point, self.area.coord_to_point, 5)
    #                 if path and path[-1] not in no0:
    #                     no0.append(path[-1])
    #                     break
    #                 path = None
    #         result.append({
    #             "ant": ant.id,
    #             "path": [{"q": step[0], "r": step[1]} for step in path]
    #         })
    #     return result

    def _generate_random_actions(self):
        result = []
        # Для каждого типа будем отслеживать куда уже кто-то пошёл или стоит
        occupied_targets = {0: set(), 1: set(), 2: set()}

        for ant in self.army.all_ants:
            ant_type = ant.type
            start_point = self.area.coord_to_point.get((ant.q, ant.r))
            if not start_point:
                continue

            # Если муравей несёт еду, он возвращается на базу
            if ant.food.amount > 0:
                print('create path')
                max_len = {0: 5, 1: 4, 2: 7}[ant_type]
                path = AntMover.createPath(
                    start_point,
                    self.area.getSpot(),
                    self.area.coord_to_point,
                    max_len
                )
                if path:
                    target_coord = path[-1]
                    if target_coord not in occupied_targets[ant_type]:
                        occupied_targets[ant_type].add(target_coord)
                    else:
                        path = None
            else:
                # Пытаемся найти путь, который не приводит к занятой клетке
                max_len = {0: 5, 1: 4, 2: 7}[ant_type]
                path = None
                for _ in range(30):
                    temp_path = AntMover.createRandomPath(start_point, self.area.coord_to_point, max_len)
                    if temp_path:
                        target_coord = temp_path[-1]
                        # (.friend is not None) and self.area.getPoint(temp_path[-1][0], temp_path[-1][1]).friend.type != ant.type
                        if (target_coord not in occupied_targets[ant_type]):
                            tmp = self.area.getPoint(temp_path[-1][0], temp_path[-1][1])
                            if tmp and tmp.friend and tmp.friend.type != ant.type:
                                path = temp_path
                                occupied_targets[ant_type].add(target_coord)
                                break

            if path:
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
