import arcade
from ..settings import HEIGHT

class EnemyLaser(arcade.Sprite):
    def __init__(self, scale=0.08, speed=-5, center_x=0, center_y=0):
        super().__init__("img/laserRay.png", scale, center_x, center_y)
        self.change_y = speed

    def update(self, delta_time):
        self.center_y += self.change_y
        if self.center_y < 0 or self.center_y > HEIGHT:
            self.remove_from_sprite_lists()
