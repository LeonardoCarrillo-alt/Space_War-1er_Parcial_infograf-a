import arcade
import random
import gameOverScreen
import winScreen

WIDTH = 1280
HEIGHT = 720
TITLE = "Space War - Nivel 3"
MOVEMENT_SPEED = 5
DEAD_ZONE = 0.2 

class Player(arcade.Sprite):
    def __init__(self, scale=0.1, center_x=0, center_y=0):
        super().__init__(
            "assets/imgScreen/navecita.png",
            scale, 
            center_x=center_x, 
            center_y=center_y
        )
        self.score = 0
        self.lives = 3  
        self.controller = None
        self.sound = arcade.load_sound("audio/8-bit-laser-151672.mp3")
        
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
        arcade.play_sound(self.sound, volume=0.2)
        print("¡Disparo realizado!")


class LaserRay(arcade.Sprite):
    def __init__(self, scale=0.1, speed=10, center_x=0, center_y=0):
        super().__init__("assets/imgScreen/laserRay.png", scale, center_x=center_x, center_y=center_y)
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
                enemy.hit_by_laser()
                enemies.remove(enemy)
                player.score += 10
                print(f"¡Enemigo destruido! Puntuación: {player.score}")
            self.remove_from_sprite_lists()
            return True
        return False


class Enemy(arcade.Sprite):
    def __init__(self, scale=1, center_x=0, center_y=0):
        enemy_images = [
            "assets/imgScreen/alien1.png",
            "assets/imgScreen/alien1.png",
            "assets/imgScreen/alien1.png",
            "assets/imgScreen/alien1.png"
        ]
        random_image = random.choice(enemy_images)
        super().__init__(random_image, scale, center_x=center_x, center_y=center_y)
        self.change_x = random.choice([-3, -2, -1, 1, 2, 3])
        self.is_hit = False
        self.fall_x = 0 
        self.fall_y = 0
        
    def update(self, delta_time: float=1/60):
        if self.is_hit: 
            self.center_x += self.fall_x
            self.center_y += self.fall_y

            if (self.top < 0 or self.right < 0 or self.left > WIDTH or self.bottom > HEIGHT):
                self.remove_from_sprite_lists()
        else: 
            self.center_x += self.change_x
            if self.left < 120:
                self.change_x = abs(self.change_x) 
            elif self.right > WIDTH - 120:
                self.change_x = -abs(self.change_x)  

    def hit_by_laser(self): 
        if not self.is_hit: 
            self.is_hit = True
            direccion = random.choice([-1, 1])
            self.fall_x = random.uniform(2, 5)*direccion
            self.fall_y = random.uniform(-8, -5)

    def shoot(self, enemy_lasers: arcade.SpriteList):
        laser = EnemyLaser(center_x=self.center_x, center_y=self.center_y)
        enemy_lasers.append(laser)


class EnemyLaser(arcade.Sprite):
    def __init__(self, scale=0.08, speed=-5, center_x=0, center_y=0):
        super().__init__("assets/imgScreen/laserRay.png", scale, center_x=center_x, center_y=center_y)
        self.change_y = speed  

    def update(self, delta_time):
        self.center_y += self.change_y
        
        if self.center_y < 0 or self.center_y > HEIGHT:
            self.remove_from_sprite_lists()


class Level3GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = None
        self.sound = None
         
        try:
            self.background = arcade.load_texture("assets/imgScreen/gamescreen.png")
        except:
            print("Error cargando el fondo")
        
        try:
            self.sound = arcade.load_sound("audio/retro-8bit-happy-adventure-videogame-music-246635.mp3")
            self.level3Sound = arcade.play_sound(self.sound, volume=0.2)
        except:
            print("Error cargando el sonido")
        
        self.sprite_list = arcade.SpriteList()
        self.enemies = arcade.SpriteList()
        self.lasers = arcade.SpriteList()
        self.enemy_lasers = arcade.SpriteList()
        
        self.player = Player(
            center_x=WIDTH // 2,
            center_y=100,
            scale=0.4
        )
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
            x_pos = random.randint(120, WIDTH - 120)  
            y_pos = random.randint(HEIGHT // 2, HEIGHT - 100)
            enemy = Enemy(center_x=x_pos, center_y=y_pos, scale=0.15)
            self.enemies.append(enemy)

    def on_update(self, delta_time):
        self.sprite_list.update()
        self.enemies.update()
        self.lasers.update()
        self.enemy_lasers.update()

        for laser in self.lasers:
            laser.check_enemies(self.enemies, self.player)
        
        for enemy in self.enemies:
            if random.random() < 0.01 and not enemy.is_hit:
                enemy.shoot(self.enemy_lasers)
        
        hits = arcade.check_for_collision_with_list(self.player, self.enemy_lasers)
        if len(self.enemies) == 0:
            level3 = winScreen.WinView()
            arcade.stop_sound(self.level3Sound)
            self.window.show_view(level3)
        if hits:
            for h in hits:
                h.remove_from_sprite_lists()
            self.player.lives -= 1
            print(f"Vidas restantes: {self.player.lives}")
            if self.player.lives <= 0:
                screenGO = gameOverScreen.GameOverView()
                arcade.stop_sound(self.level3Sound)
                self.window.show_view(screenGO)
        
        active_enemies = [enemy for enemy in self.enemies if not enemy.is_hit]
            
       

    def on_draw(self):
        self.clear()
        
        if self.background:
            arcade.draw_texture_rect( self.background,arcade.LRBT(0, WIDTH, 0, HEIGHT))
        else:
            arcade.set_background_color(arcade.color.BLACK)
        
        self.sprite_list.draw()
        self.enemies.draw()
        self.lasers.draw()
        self.enemy_lasers.draw()
        
        arcade.draw_text(
            f"Score: {self.player.score}",
            20,
            HEIGHT - 40,
            arcade.color.AERO_BLUE,
            font_size=25
        )
        
        arcade.draw_text(
            f"Lives: {self.player.lives}",
            20,
            HEIGHT - 80,
            arcade.color.RED,
            font_size=25
        )

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
            
    def on_joybutton_press(self, joystick, button):
        print(f"Botón presionado: {button}")
        self.last_button_pressed = str(button)
        
        self.player.shoot(self.lasers)
            
    def on_joybutton_release(self, joystick, button):
        print(f"Botón liberado: {button}")
        
    def on_joyaxis_motion(self, joystick, axis, value):
        if axis == "x":
            if abs(value) < DEAD_ZONE:
                self.player.change_x = 0
            else:
                self.player.change_x = value * MOVEMENT_SPEED
                
    def on_joyhat_motion(self, joystick, hat_x, hat_y):
        print(f"Hat movido: {hat_x}, {hat_y}")
