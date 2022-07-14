from PyQt5 import Qt
from PyQt5.QtGui import QPainter, QPen, QBrush
from PyQt5.QtWidgets import QWidget


class Healthbar:
    def __init__(self, window: QWidget, x: int, y: int, width: int, height: int, initial_health: int):
        self.window = window
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.initial_health = initial_health
        self.current_health = initial_health-50

    def paint(self):
        painter = QPainter(self.window)
        painter.setBrush(QBrush(Qt.Qt.red, Qt.Qt.DiagCrossPattern))
        painter.drawRect(self.x, self.y, self.current_health/self.initial_health*self.width, self.height)

        painter.setBrush(QBrush(Qt.Qt.NoBrush))
        painter.setPen(QPen(Qt.Qt.black, 5, Qt.Qt.SolidLine))
        # painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        painter.drawRect(self.x, self.y, self.width, self.height)


