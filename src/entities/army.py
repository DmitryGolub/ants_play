from charset_normalizer.cd import alphabet_languages

from src.entities.area import Ant, Food

class Army:
    busy_ants = []
    busy_targets = []
    idle_ants = []
    all_ants = []
    def __init__(self):
        pass

    def updateArmy(self, ants):
        self.all_ants = self.parse_ants(ants)
        new_busy_ants = []
        new_busy_targets = []

        for ant, target in zip(self.busy_ants, self.busy_targets):
            current_ant = self._find_ant_by_id(ant.id)
            if current_ant is None:
                continue  # муравей погиб

            if (current_ant.q, current_ant.r) == target:
                self.idle_ants.append(current_ant)  # цель достигнута
            else:
                new_busy_ants.append(current_ant)
                new_busy_targets.append(target)

        self.busy_ants = new_busy_ants
        self.busy_targets = new_busy_targets

        busy_ids = {ant.id for ant in self.busy_ants}
        self.idle_ants = [
            ant for ant in self.all_ants
            if ant.id not in busy_ids
        ]

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

    def add_busy_ant(self):
        pass
    def remove_budy_ant(self):
        pass