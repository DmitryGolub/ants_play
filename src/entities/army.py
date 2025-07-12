from src.entities.area import Ant, Food

class Army:
    busy_ants = []
    idle_ants = []

    def __init__(self):
        pass

    def updateArmy(self, ants):
        print(ants)
        tmp_ants = Army.parse_ants(ants)
        pass

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

    def add_busy_ant(self):
        pass
    def remove_budy_ant(self):
        pass