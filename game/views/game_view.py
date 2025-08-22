import arcade
import random
from ..settings import WIDTH, HEIGHT, DEAD_ZONE, MOVEMENT_SPEED
from ..models.player import Player
from ..services.enemy_spawner import EnemySpawner
from ..services.collision_service import CollisionService

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.ARCADE_GREEN
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.laser_list = arcade.SpriteList()
        self.enemy_laser_list = arcade.SpriteList()

        self.player = Player(center_x=WIDTH//2, center_y=HEIGHT//4.5)
        self.player_list.append(self.player)

        EnemySpawner.spawn(self.enemy_list)

        # Configurar el control
        self.setup_controller()

        # Texto de instrucciones
        self.instruction_text = "Usa el joystick izquierdo para moverte | X para disparar" if self.player.controller else "Flechas para moverte | Espacio para disparar"

        # Para debug: mostrar información de botones
        self.last_button_pressed = "Ninguno"

    def setup_controller(self):
        """Configurar el control y registrar manejadores en la vista principal"""
        if self.player.controller:
            # Registrar los manejadores en la vista principal, no en el sprite
            self.player.controller.push_handlers(self)
            #print("Control configurado en la vista del juego")

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
                #Se modificaran el game over
                print("game Over")
                fail_view = DifficultyView()
                self.window.show_view(fail_view)

    def on_draw(self):
        self.clear()
        self.player_list.draw()
        self.enemy_list.draw()
        self.laser_list.draw()
        self.enemy_laser_list.draw()

        arcade.draw_text(f"Score: {self.player.score}", 20, HEIGHT - 40,
                         arcade.color.AERO_BLUE, font_size=25)

        arcade.draw_text(
            self.instruction_text,
            20,
            HEIGHT - 80,
            arcade.color.LIGHT_GRAY,
            font_size=16)
         
        arcade.draw_text(
            f"Vidas: {self.player.lives}",
            20,
            HEIGHT - 120,
            arcade.color.YELLOW,
            font_size=16)

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

    def on_joybutton_press(self, controller, button):
        print(f"Botón presionado en la vista: {button}")
        self.last_button_pressed = button

        if button == "x":
            self.player.shoot(self.laser_list)
            print("Disparando con botón X del control")
        elif button == "a":
            self.player.shoot(self.laser_list)
            print("Disparando con botón A del control")
        elif button == "0":
            self.player.shoot(self.laser_list)
            print("Disparando con botón 0 del control")

        self.player.shoot(self.laser_list)

    def on_joybutton_release(self, controller, button):
        print(f"Botón liberado: {button}")

    def on_joyaxis_motion(self, controller, axis, value):
        # Solo eje X para movimiento horizontal
        if axis == "x":
            # Aplicar zona muerta
            if abs(value) < DEAD_ZONE:
                self.player.change_x = 0
            else:
                self.player.change_x = value * MOVEMENT_SPEED

    def on_joyhat_motion(self, controller, hat_x, hat_y):
        print(f"Hat movido: {hat_x}, {hat_y}")