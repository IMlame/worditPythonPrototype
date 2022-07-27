from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem

from custom_widgets import Healthbar
from custom_widgets.AttributeHandler import AttributeHandler


class Player:
    def __init__(self, window: QWidget, enemy_img: str, img_height: int, healthbar: Healthbar):
        self.attributes = []

        self.img_height = img_height

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
        return self.healthbar.current_health == 0

    # check for status effects
    def attack(self, damage: int):
        return damage

    def update(self):
        self.healthbar.paint()

    def is_dead(self):
        if self.healthbar.current_health == 0:
            self.pixmap.setPixmap(QPixmap("assets/player2.png").scaledToWidth(self.img_height))
        return self.healthbar.current_health == 0

    def reset(self, new_max_health: int):
        self.healthbar.reset_heatlh(new_max_health=new_max_health)