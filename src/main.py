from src.entities.army import Army
from src.entities.area import Area
from src.entities.strategy import Strategy
from src.lib import sender, getter

step = 0

while True:
    ans = sender("register")
    print(ans)
    data = getter("arena")
    area = Area()
    area.updateArea(data)
    area.print_map()