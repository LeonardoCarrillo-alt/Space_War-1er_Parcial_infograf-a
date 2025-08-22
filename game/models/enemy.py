import arcade
import random
from ..settings import WIDTH, HEIGHT
from ..models.enemy_laser import EnemyLaser

class Enemy(arcade.Sprite):
    def __init__(self, scale=1, center_x=0, center_y=0):
        super().__init__("img/coin.png", scale, center_x, center_y)
        self.change_x = random.choice([-3, -2, -1, 1, 2, 3])

    def update(self, delta_time: float = 1/60):
        self.center_x += self.change_x

        if self.left < 20:
            self.change_x = abs(self.change_x)  # Cambiar a dirección positiva
        elif self.right > WIDTH - 20:
            self.change_x = -abs(self.change_x)  # Cambiar a dirección negativa

    def shoot(self, enemy_lasers: arcade.SpriteList):
        enemy_lasers.append(EnemyLaser(center_x=self.center_x, center_y=self.center_y))
