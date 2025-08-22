import arcade
import random

WIDTH = 1280
HEIGHT = 720
TITLE = "Space War - Nivel 1"
MOVEMENT_SPEED = 5
DEAD_ZONE = 0.2 

class Player(arcade.Sprite):
    def __init__(self, scale=0.1, center_x=0, center_y=0):
        super().__init__(
            "assets/imgScreen/navecita.png",
            scale, center_x, center_y)
        self.score = 0
        self.controller = None
        self.game_view = None  
        
        controllers = arcade.get_game_controllers()
        print(f"Encontrados {len(controllers)} controles!")
        
        if controllers:
            self.controller = controllers[0]
            self.controller.open()
            print("Conectado a un control")

    def update(self, delta_time: float = 1 / 60):
        self.center_x += self.change_x
        
       
        if self.center_x < 120:
            self.center_x = 120
        if self.center_x > WIDTH - 120:
            self.center_x = WIDTH - 120

    def shoot(self, laser_list: arcade.SpriteList):
        new_laser = LaserRay(center_x=self.center_x, center_y=self.center_y)
        laser_list.append(new_laser)
        print("¡Disparo realizado!")


class LaserRay(arcade.Sprite):
    def __init__(self, scale=0.1, speed=10, center_x=0, center_y=0):
        super().__init__("assets/imgScreen/laserRay.png", scale, center_x, center_y)
        self.change_y = speed
        self.bottom = center_y + 30  

    def update(self, delta_time):
        self.center_y += self.change_y
        
        if self.bottom > HEIGHT:
            self.remove_from_sprite_lists()

    def check_enemies(self, enemies: arcade.SpriteList, player: "Player"):
        hit_list = arcade.check_for_collision_with_list(self, enemies)
        if hit_list:
            for enemy in hit_list:
                enemies.remove(enemy)
                player.score += 10
                print(f"¡Enemigo destruido! Puntuación: {player.score}")
            self.remove_from_sprite_lists()
            return True
        return False


class Enemy(arcade.Sprite):
    def __init__(self, scale=1, center_x=0, center_y=0):
        super().__init__(
            "assets/imgScreen/alien1.png",
            scale, center_x, center_y)
        self.change_x = random.choice([-3, -2, -1, 1, 2, 3])
        
    def update(self, delta_time: float=1/60):
        self.center_x += self.change_x

        if self.left < 70:
            self.change_x = abs(self.change_x) 
        elif self.right > WIDTH - 70:
            self.change_x = -abs(self.change_x)  


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture("assets/imgScreen/gamescreen.png")
        self.sound = arcade.load_sound("audio/retro-8bit-happy-adventure-videogame-music-246635.mp3")

        arcade.play_sound(self.sound, volume=0.2)
        
        self.sprite_list = arcade.SpriteList()
        self.enemies = arcade.SpriteList()
        self.lasers = arcade.SpriteList()
        self.player = Player(
            center_x=WIDTH // 2,
            center_y=100,
            scale=0.4
        )
        self.player.game_view = self  
        self.sprite_list.append(self.player)
        self.spawn_enemies()
        
        self.setup_controller()
        
        self.last_button_pressed = "Ninguno"

    def setup_controller(self):
        if self.player.controller:
            self.player.controller.push_handlers(self)
            print("Control configurado en la vista del juego")

    def spawn_enemies(self):
        num_enemies = random.randint(10, 15)
        for _ in range(num_enemies):
            x_pos = random.randint(50, WIDTH - 50)
            y_pos = random.randint(HEIGHT // 2, HEIGHT - 100)
            enemy = Enemy(center_x=x_pos, center_y=y_pos, scale=0.15)
            self.enemies.append(enemy)

    def on_update(self, delta_time):
        self.sprite_list.update(delta_time)
        self.enemies.update(delta_time)
        self.lasers.update(delta_time)

        for laser in self.lasers:
            laser.check_enemies(self.enemies, self.player)
            
        if len(self.enemies) == 0:
            self.spawn_enemies()

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background, arcade.LRBT(0, WIDTH, 0, HEIGHT))
        self.sprite_list.draw()
        self.enemies.draw()
        self.lasers.draw()
        
        arcade.draw_text(
            f"Score: {self.player.score}",
            20,
            HEIGHT - 40,
            arcade.color.AERO_BLUE,
            font_size=25)
            

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.RIGHT:
            self.player.change_x = MOVEMENT_SPEED
        elif symbol == arcade.key.LEFT:
            self.player.change_x = -MOVEMENT_SPEED
        elif symbol == arcade.key.SPACE:
            self.player.shoot(self.lasers)
            self.last_button_pressed = "ESPACIO (teclado)"

    def on_key_release(self, symbol, modifiers):
        if symbol in [arcade.key.LEFT, arcade.key.RIGHT]:
            self.player.change_x = 0
            
    def on_joybutton_press(self, controller, button):
        print(f"Botón presionado en la vista: {button}")
        self.last_button_pressed = button
        
        if button == "x": 
            self.player.shoot(self.lasers)
            print("Disparando con botón X del control")
        elif button == "a":  
            self.player.shoot(self.lasers)
            print("Disparando con botón A del control")
        elif button == "0": 
            self.player.shoot(self.lasers)
            print("Disparando con botón 0 del control")
            
        
        self.player.shoot(self.lasers) 
        
    def on_joybutton_release(self, controller, button):
        print(f"Botón liberado: {button}")
        
    def on_joyaxis_motion(self, controller, axis, value):
        if axis == "x":
            if abs(value) < DEAD_ZONE:
                self.player.change_x = 0
            else:
                self.player.change_x = value * MOVEMENT_SPEED
                
    def on_joyhat_motion(self, controller, hat_x, hat_y):
        print(f"Hat movido: {hat_x}, {hat_y}")


def main():
    window = arcade.Window(WIDTH, HEIGHT, TITLE)
    game = GameView()
    window.show_view(game)
    arcade.run()


if __name__ == "__main__":
    main()