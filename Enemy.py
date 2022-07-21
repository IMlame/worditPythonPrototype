import time

from PyQt5.QtGui import QPixmap
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QLabel, QWidget

from Healthbar import Healthbar


class Enemy:
    def __init__(self, window: QWidget, enemy_img: str, img_height: int, healthbar: Healthbar):
        self.healthbar = healthbar
        pixmap = QPixmap(enemy_img)
        self.image = QLabel(window)
        self.image.setPixmap(pixmap.scaledToWidth(img_height))
        self.image.move(int((healthbar.width-healthbar.x)/2 - self.image.width()), int(healthbar.y - img_height))

    def damage(self, damage: int):
        self.healthbar.damage(damage=damage)

    def update(self):
        self.healthbar.paint()

    def apply_status_effect(self, status_effect: str):
        # keep track of status effects on enemy here
        pass

    def attack(self):
        # return damage and status effects on player
        return 5
