from PyQt5.Qt import Qt
from PyQt5.QtGui import QPainter, QPen, QBrush
from PyQt5.QtWidgets import QWidget, QLabel


class Healthbar:
    def __init__(self, window: QWidget, x: int, y: int, width: int, height: int, initial_health: int, color):
        self.window = window
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.initial_health = initial_health
        self.current_health = initial_health
        self.color = color

        self.health_label = QLabel(window)
        self.health_label.move(self.x, self.y)
        self.health_label.setText(str(self.current_health) + " / " + str(self.initial_health))

    def paint(self):
        painter = QPainter(self.window)
        painter.setBrush(QBrush(self.color, Qt.FDiagPattern))
        painter.drawRect(self.x, self.y, int((self.current_health / self.initial_health) * self.width), self.height)

        painter.setBrush(QBrush(Qt.NoBrush))
        painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))
        # painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        painter.drawRect(self.x, self.y, self.width, self.height)

        self.health_label.setText(str(self.current_health) + " / " + str(self.initial_health))
        self.health_label.adjustSize()

    def damage(self, damage: int):
        # keeps health in range of 0 to full health
        self.current_health = min(max(self.current_health - damage, 0), self.initial_health)
        return self.current_health == 0

    def reset_heatlh(self, new_max_health: int):
        self.current_health = new_max_health
        self.initial_health = new_max_health
