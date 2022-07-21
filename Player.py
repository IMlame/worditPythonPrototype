from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel

import Healthbar


class Player:
    def __init__(self, window: QWidget, enemy_img: str, img_height: int, healthbar: Healthbar):
        self.healthbar = healthbar
        pixmap = QPixmap(enemy_img)
        image = QLabel(window)
        image.setPixmap(pixmap.scaledToWidth(img_height))
        image.move(int((healthbar.width-healthbar.x)/2 - image.width()), int(healthbar.y - img_height))

    def damage(self, damage: int):
        self.healthbar.damage(damage=damage)

    def update(self):
        self.healthbar.paint()