from src.entities.area import Ant, Food, Point

class Army:
    busy_ants = []
    idle_ants = []
    all_ants = []
    busy_targets = []
    def __init__(self):
        pass

    def updateArmy(self, ants):
        self.all_ants = self.parse_ants(ants)
        self.idle_ants = self.all_ants.copy()
        self.busy_ants = []
        self.busy_targets = []

    def _find_ant_by_id(self, ant_id: str) -> Ant | None:
        for ant in self.all_ants:
            if ant.id == ant_id:
                return ant
        return None

    @staticmethod
    def parse_ants(data: list[dict]) -> list[Ant]:
        ants = []
        for ant_data in data:
            food_data = ant_data.get('food')
            food = None
            if food_data:
                food = Food(
                    q=ant_data['q'],
                    r=ant_data['r'],
                    type=food_data.get('type', 0),
                    amount=food_data.get('amount', 0)
                )
            ant = Ant(
                q=ant_data['q'],
                r=ant_data['r'],
                type=ant_data['type'],
                health=ant_data['health'],
                id=ant_data['id'],
                food=food
            )
            ants.append(ant)
        return ants

    def add_busy_ant(self, ant: Ant):
        if ant in self.idle_ants:
            self.idle_ants.remove(ant)
        self.busy_ants.append(ant)

    def remove_busy_ant(self):
        pass