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
        return []