from src.entities.area import Area
from src.entities.ant import AntMover
from src.entities.army import Army


class Strategy:
    def init(self, Area: Area, Mover: AntMover, Army: Army):
        pass

    def setArea(self, newarea):
        self.area = newarea
