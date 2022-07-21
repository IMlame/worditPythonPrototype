from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel

from custom_widgets import Healthbar
from custom_widgets.AttributeHandler import AttributeHandler


class Player:
    def __init__(self, window: QWidget, enemy_img: str, img_height: int, healthbar: Healthbar):
        self.attributes = []

        self.healthbar = healthbar

        # attribute handler
        self.attribute_handler = AttributeHandler(window=window, x=self.healthbar.x, y=self.healthbar.y - 25)

        pixmap = QPixmap(enemy_img)
        image = QLabel(window)
        image.setPixmap(pixmap.scaledToWidth(img_height))
        image.move(int(((healthbar.width-healthbar.x) - image.width())/2), int(healthbar.y - img_height))

    def damage(self, damage: int):
        self.healthbar.damage(damage=damage)
        return self.healthbar.current_health == 0

    # check for status effects
    def attack(self, damage: int):
        return damage

    def update(self):
        self.healthbar.paint()