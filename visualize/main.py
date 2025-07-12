import sys
import time
import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import QTimer
import matplotlib
matplotlib.use('QtAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.patches as patches
import numpy as np
from src.env import FILENAME

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
            1: "#b5e7a0",   # муравейник (зелёный)
            2: "#ffdac1",   # пустой (бежевый)
            3: "#e0bbf3",   # грязь (фиолетовый)
            4: "#fdffb6",   # кислота (жёлтый)
            5: "#b0b0b0",   # камни (серый)
        }
        default_color = "#eeeeee"

        # Рисуем клетки
        for tile in arena.get("map", []):
            q, r, ttype = tile["q"], tile["r"], tile["type"]
            x, y = hex_to_pixel(q, r)
            color = tile_colors.get(ttype, default_color)
            hex_patch = patches.RegularPolygon((x, y), numVertices=6, radius=1,
                                               orientation=np.radians(30), edgecolor="gray", facecolor=color)
            self.ax.add_patch(hex_patch)

        for food in arena.get("food", []):
            x, y = hex_to_pixel(food["q"], food["r"])
            self.ax.plot(x, y, marker='o', markersize=20, color='red', alpha=0.7)
            self.ax.text(x, y, str(food["amount"]), va="center", ha="center", fontsize=10, color='white')

        for home in arena.get("home", []):
            x, y = hex_to_pixel(home["q"], home["r"])
            self.ax.plot(x, y, marker='s', markersize=20, color='blue', alpha=0.5)

        ant_colors = {
            0: "black",    # рабочий
            1: "green",    # боец
            2: "orange",   # скаут
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
        self.draw()

class MainWindow(QMainWindow):
    def __init__(self, json_path, interval=1000):
        super().__init__()
        self.setWindowTitle("Ants Arena Viewer")
        self.canvas = ArenaCanvas(self)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.json_path = json_path
        self.interval = interval

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_arena)
        self.timer.start(self.interval)
        self.update_arena()

    def update_arena(self):
        try:
            with open(self.json_path, encoding="utf-8") as f:
                arena = json.load(f)
            self.canvas.draw_arena(arena)
        except Exception as e:
            print("Ошибка чтения файла:", e)

if __name__ == "__main__":
    json_path = FILENAME
    app = QApplication(sys.argv)
    window = MainWindow(json_path)
    window.show()
    sys.exit(app.exec())
