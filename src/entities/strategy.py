from src.entities.area import Area
from src.entities.ant import AntMover
from src.entities.army import Army


class Strategy:
    def __init__(self):
        pass

    def update_state(self, army: Army, area: Area):
        self.army = army
        self.area = area

    def generate_actions(self):
        print('generationg actions:')
        a = self._generate_def_actions()
        b = self._generate_food_actions()
        c = self._generate_attack_actions()
        d = self._generate_idle_actions()
        return a + b + c + d
    
    def _generate_def_actions(self):
        return []
    def _generate_food_actions(self):
        return []
    def _generate_attack_actions(self):
        return []
    def _generate_idle_actions(self):
        return []

    def nearest_food_ant(self):
        pass

    def send_ant(self):
        pass

    def def_orechnik(self):
        pass

    def check_def(self):
        pass