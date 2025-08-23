import arcade
from ..models.laser import LaserRay
from ..settings import MOVEMENT_SPEED

class Player(arcade.Sprite):
    def __init__(self, scale=0.4, center_x=0, center_y=0):
        super().__init__("assets/imgScreen/navecita.png", scale, center_x, center_y)
        self.score = 0
        self.lives = 3

    def update(self, delta_time: float = 1/60):
        self.center_x += self.change_x
        self.center_y += self.change_y

    def shoot(self, laser_list: arcade.SpriteList):
        laser_list.append(LaserRay(center_x=self.center_x, center_y=self.center_y))

    def move_left(self):
        self.change_x = -MOVEMENT_SPEED

    def move_right(self):
        self.change_x = MOVEMENT_SPEED

    def stop(self):
        self.change_x = 0
