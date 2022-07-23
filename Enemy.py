from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QWidget, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem

from custom_widgets.AttributeHandler import AttributeHandler
from custom_widgets.Healthbar import Healthbar


class Enemy:
    def __init__(self, window: QWidget, enemy_img: str, img_height: int, healthbar: Healthbar, base_dmg=5):
        self.base_dmg = base_dmg

        self.img_height = img_height

        # healthbar
        self.healthbar = healthbar

        # attribute handler
        self.attribute_handler = AttributeHandler(window=window, x=self.healthbar.x, y=self.healthbar.y - 25)

        # image code
        graphics_view = QGraphicsView(window)
        scene = QGraphicsScene()
        self.pixmap = QGraphicsPixmapItem()
        scene.addItem(self.pixmap)
        graphics_view.setScene(scene)
        self.pixmap.setPixmap(QPixmap(enemy_img).scaledToWidth(img_height))
        graphics_view.move(int(((healthbar.width - healthbar.x) - self.pixmap.pixmap().width()) / 2),
                           int(healthbar.y - img_height))
        graphics_view.setStyleSheet("background:transparent")

    def damage(self, damage: int):
        self.healthbar.damage(damage=damage)
        self.pixmap.setPixmap(QPixmap("assets/enemy2.png").scaledToWidth(self.img_height))
        return self.healthbar.current_health == 0

    def update(self):
        self.healthbar.paint()

    def apply_status_effect(self, status_effect: str):
        self.attribute_handler.add_effect(status_effect)

    def attack(self):
        # return damage and status effects on player
        dmg = self.base_dmg

        attributes = self.attribute_handler.get_attributes()

        # handle special effects
        keep_attributes = False
        for attribute in attributes:
            if "FREZ" in attribute:
                dmg = 0
            elif "BURN" in attribute:
                self.healthbar.damage(3 * int(attribute[-1]))
            elif "WEAK" in attribute:
                dmg = (dmg / int(attribute[-1]))
            elif "PARA" in attribute:
                dmg = 0
                keep_attributes = True

        if not keep_attributes:
            self.attribute_handler.clear_attributes()

        self.pixmap.setPixmap(QPixmap("assets/enemy.png").scaledToWidth(self.img_height))
        return dmg

    def is_dead(self):
        return self.healthbar.current_health == 0

    def reset(self, new_max_health: int, new_base_damage: int):
        self.healthbar.reset_heatlh(new_max_health=new_max_health)
        self.base_dmg = new_base_damage
        self.attribute_handler.clear_attributes()