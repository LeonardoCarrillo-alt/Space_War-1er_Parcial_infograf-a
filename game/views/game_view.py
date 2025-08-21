import arcade
import random
from ..settings import WIDTH, HEIGHT
from ..models.player import Player
from ..services.enemy_spawner import EnemySpawner
from ..services.collision_service import CollisionService

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.BLACK
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.laser_list = arcade.SpriteList()
        self.enemy_laser_list = arcade.SpriteList()

        self.player = Player(center_x=WIDTH//4.5, center_y=HEIGHT//4.5)
        self.player_list.append(self.player)

        EnemySpawner.spawn(self.enemy_list)

    def on_update(self, delta_time):
        self.player_list.update(delta_time)
        self.enemy_list.update(delta_time)
        self.laser_list.update(delta_time)
        self.enemy_laser_list.update(delta_time)

        for laser in self.laser_list:
            laser.check_collision(self.enemy_list, self.player)

        for enemy in self.enemy_list:
            if random.random() < 0.01:
                enemy.shoot(self.enemy_laser_list)

        if CollisionService.check_player_hit(self.player, self.enemy_laser_list):
            print(f"Vidas restantes: {self.player.lives}")
            if self.player.lives <= 0:
                print("Game Over")
                arcade.close_window()

    def on_draw(self):
        self.clear()
        self.player_list.draw()
        self.enemy_list.draw()
        self.laser_list.draw()
        self.enemy_laser_list.draw()

        arcade.draw_text(f"Score: {self.player.score}", 20, HEIGHT-40,
                         arcade.color.AERO_BLUE, font_size=25)

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.RIGHT:
            self.player.move_right()
        elif symbol == arcade.key.LEFT:
            self.player.move_left()
        elif symbol == arcade.key.SPACE:
            self.player.shoot(self.laser_list)

    def on_key_release(self, symbol, modifiers):
        if symbol in [arcade.key.LEFT, arcade.key.RIGHT]:
            self.player.stop()
