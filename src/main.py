import time

from src.entities.army import Army
from src.entities.area import Area
from src.entities.strategy import Strategy
from src.lib import sender, getter


def try_register_until_success():
    print("Пробуем зарегистрироваться на раунд...")
    while True:
        ans = sender("register")
        if "lobbyEndsIn" in ans:
            if ans['lobbyEndsIn'] < 0:
                print('Раунд уже идёт')
                return False
            else:
                print(f"Успешная регистрация! До начала раунда: {ans['lobbyEndsIn']} секунд")
                return ans
        else:
            print("Регистрация пока не открыта. Повтор через 5 секунд...")
            time.sleep(5)

def wait_for_round_start(lobbyEndsIn: int):
    print(f"Ожидание начала раунда ({lobbyEndsIn} сек)...")
    time.sleep(lobbyEndsIn)

def play_round():
    last_turn = -1
    area = Area()
    army = Army()
    strategy = Strategy()

    while True:
        data = getter("arena")

        current_turn = data.get("turnNo")
        if current_turn == last_turn:
            time.sleep(1)
            continue

        last_turn = current_turn
        print(f"Ход #{current_turn}")

        area.updateArea(data)
        army.updateArmy(data['ants'])
        strategy.update_state(army, area)
        actions = strategy.generate_actions()

        if actions:
            result = sender("actions", actions)
        else:
            print("Код писал даун")

        time.sleep(1)

# Главный цикл
while True:
    reg_data = try_register_until_success()
    if reg_data:
        wait_for_round_start(reg_data["lobbyEndsIn"])
    play_round()
