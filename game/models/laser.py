import arcade
from ..settings import WIDTH, HEIGHT

class LaserRay(arcade.Sprite):
    def __init__(self, scale=0.1, speed=10, center_x=0, center_y=0):
        super().__init__("img/laserRay.png", scale, center_x, center_y)
        self.change_y = speed

    def update(self, delta_time):
        #self.center_x += self.change_x
        self.center_y += self.change_y

        if self.center_y > HEIGHT: #or self.center_x < 0 or self.center_x > WIDTH:
            self.remove_from_sprite_lists()

    def check_collision(self, enemies: arcade.SpriteList, player: "Player"):
        hit_list = arcade.check_for_collision_with_list(self, enemies)
        if hit_list:
            for enemy in hit_list:
                enemy.remove_from_sprite_lists()
                player.score += 10
            self.remove_from_sprite_lists()
