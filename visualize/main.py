import sys
import requests
import json
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import QThread, pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import time

#
# def data_to_json(data, file: str) -> None:
#     with open(file, "w", encoding="utf-8") as file:
#         json.dump(data, file, indent=4, ensure_ascii=False)
#
#
# with requests.Session() as session:
#     headers = {
#         'accept': 'application/json',
#         'X-Auth-Token': 'e71c6ce6-f297-40fb-9a44-16b650933bec'
#     }
#
#     register = session.post(
#         url="https://games-test.datsteam.dev/api/register",
#         headers=headers
#     )
#
#     if register.status_code == 200:
#         print("Success authenticate")
#     else:
#         print("Unsuccess authenticate")
#         print(register)
#         raise TimeoutError("Register was finished, wait new game")

    # data_to_json(register.json(), "register.json")
    #
    # arena = session.get(
    #     url="https://games-test.datsteam.dev/api/arena",
    #     headers=headers
    # ).json()
    #
    # data_to_json(arena, "arena.json")
    #
    # logs = session.post(
    #     url="https://games-test.datsteam.dev/api/register",
    #     headers=headers
    # ).json()
    #
    # data_to_json(logs, "logs.json")
    #
    # data_move = {
    #     "moves": [
    #         {
    #             "ant": "11111111-2222-3333-4444-555555555555",
    #             "path": [
    #                 {
    #                     "q": 10,
    #                     "r": 20
    #                 }
    #             ]
    #         }
    #     ]
    # }
    #
    # move = session.post(
    #     url="https://games-test.datsteam.dev/api/register",
    #     headers=headers
    # ).json()


    #
    # print("Finish pars")




def hex_to_pixel(q, r, size=1):
    x = size * (3/2 * q)
    y = size * (np.sqrt(3) * (r + q/2))
    return (x, y)

class ArenaCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        super().__init__(self.fig)
        self.setParent(parent)
        self.ax.set_aspect('equal')
        self.ax.axis('off')

    def draw_arena(self, arena):
        self.ax.clear()
        self.ax.set_aspect('equal')
        self.ax.axis('off')

        tile_colors = {
            1: "#b5e7a0",   # grass зеленый
            2: "#ffdac1",   # sand оранжевый
            3: "#e0bbf3",   # stone фиолетовый
            4: "#fdffb6"    # water желтый
        }
        default_color = "#eeeeee" # серый

        for tile in arena["map"]:
            q, r, ttype = tile["q"], tile["r"], tile["type"]
            x, y = hex_to_pixel(q, r)
            color = tile_colors.get(ttype, default_color)
            hex_patch = patches.RegularPolygon((x, y), numVertices=6, radius=1, orientation=np.radians(30), edgecolor="gray", facecolor=color)
            self.ax.add_patch(hex_patch)

        for food in arena.get("food", []):
            x, y = hex_to_pixel(food["q"], food["r"])
            self.ax.plot(x, y, marker='o', markersize=20, color='red', alpha=0.7)
            self.ax.text(x, y, str(food["amount"]), va="center", ha="center", fontsize=10, color='white')

        for home in arena.get("home", []):
            x, y = hex_to_pixel(home["q"], home["r"])
            self.ax.plot(x, y, marker='s', markersize=20, color='blue', alpha=0.5)

        ant_colors = {
            0: "black",    # свой тип
            1: "green",    # союзник
            2: "orange",   # ещё тип
        }
        for ant in arena.get("ants", []):
            x, y = hex_to_pixel(ant["q"], ant["r"])
            color = ant_colors.get(ant["type"], "gray")
            self.ax.plot(x, y, marker='P', markersize=25, color=color)
            self.ax.text(x, y+0.3, f"{ant['health']}", ha="center", fontsize=9, color=color)

        for enemy in arena.get("enemies", []):
            x, y = hex_to_pixel(enemy["q"], enemy["r"])
            self.ax.plot(x, y, marker='X', markersize=18, color='red')

        self.ax.set_title(f"Turn: {arena.get('turnNo', 0)}  Score: {arena.get('score', 0)}")
        self.draw()  # обновить

class ArenaUpdateThread(QThread):
    arena_data_signal = pyqtSignal(dict)

    def __init__(self, interval=1):
        super().__init__()
        self.interval = interval
        self.running = True

    def run(self):
        while self.running:
            try:
                with open("../data/arena.json", encoding="utf-8") as f:
                    arena = json.load(f)
                self.arena_data_signal.emit(arena)
            except Exception as e:
                print("Ошибка чтения файла:", e)
            time.sleep(self.interval)

    def stop(self):
        self.running = False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ants Arena Live Viewer")
        self.canvas = ArenaCanvas(self)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # поток для обновления данных (работает всегда, даже если окно не в фокусе)
        self.update_thread = ArenaUpdateThread()
        self.update_thread.arena_data_signal.connect(self.canvas.draw_arena)
        self.update_thread.start()

    def closeEvent(self, event):
        self.update_thread.stop()
        self.update_thread.wait()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
