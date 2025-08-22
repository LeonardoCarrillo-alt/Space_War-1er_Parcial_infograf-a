import random
from game.settings import WIDTH, HEIGHT
from ..models.enemy import Enemy

class EnemySpawner:
    @staticmethod
    def spawn(enemies: "arcade.SpriteList", count: int = None):

        num_enemies = random.randint(10, 15)
        for _ in range(num_enemies):
            x_pos = random.randint(50, WIDTH - 50)
            y_pos = random.randint(HEIGHT // 2, HEIGHT - 100)
            enemies.append(Enemy(center_x=x_pos, center_y=y_pos, scale=0.15))