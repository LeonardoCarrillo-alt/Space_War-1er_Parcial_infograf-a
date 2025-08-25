import arcade
import random
import gameOverScreen
import Level3
import time

WIDTH = 1280
HEIGHT = 720
TITLE = "Space War - Nivel 2"
MOVEMENT_SPEED = 5
DEAD_ZONE = 0.2 
LEVEL_TIME = 40

class Player(arcade.Sprite):
    def __init__(self, scale=0, center_x=0, center_y=0):
        super().__init__(
            "assets/imgScreen/navecita.png",
            scale, center_x, center_y)
        self.score = 0
        self.controller = None
        self.lives = 3

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

    def shoot(self, laser: arcade.SpriteList):
        laser.append(LaserRay(center_x=self.center_x, center_y=self.center_y))
        self.shootSound = arcade.load_sound("audio/8-bit-laser-151672.mp3")
        arcade.play_sound(self.shootSound, volume=0.2)

class LaserRay(arcade.Sprite):
    def __init__(self, scale= 0.1, speed=10, center_x=0, center_y=0):
        super().__init__("assets/imgScreen/laserRay.png", scale, center_x, center_y)
        self.change_y = speed

    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y
        
        if self.center_x > WIDTH or self.center_x < 0 or self.center_y > HEIGHT:
            self.remove_from_sprite_lists()  

    def check_enemies(self, enemies: arcade.SpriteList,  destroyed_enemies: arcade.SpriteList , player: "Player"):
        for enemy in enemies:
            
            if (
                    abs(self.center_x - enemy.center_x) < 20 and
                    abs(self.center_y - enemy.center_y) < 20
            ):
                enemy.destroyed = True
                destroyed_enemy = DestroyedEnemy(enemy.center_x, enemy.center_y, scale = 1)
                destroyed_enemies.append(destroyed_enemy)
                enemies.remove(enemy)
                self.remove_from_sprite_lists() 
                player.score += 10
                break  


class DestroyedEnemy(arcade.Sprite): 
    def __init__(self, center_x, center_y, scale=1):
        super().__init__("assets/imgScreen/explode.png", scale, center_x, center_y)
        self.creation_time = time.time() 
        self.playBoom = arcade.load_sound("audio/retro-explode-1-236678.mp3")
        arcade.play_sound(self.playBoom, volume=0.2)
    def update(self, delta_time=0):
        if time.time() - self.creation_time > 1:
            self.remove_from_sprite_lists()


class Enemy(arcade.Sprite):
    def __init__(self, scale = 1, center_x = 0, center_y = 0):
        ALIEN_SPRITES = [
            "assets/imgScreen/alien1.png",
            "assets/imgScreen/alien2.1.png",
            "assets/imgScreen/alien3.1.png",
            "assets/imgScreen/alien4.png",
            "assets/imgScreen/alien5.1.png"
        ]
        random_sprite = random.choice(ALIEN_SPRITES)
        super().__init__(random_sprite, scale, center_x, center_y)
        self.change_x = random.choice([-3, -2, -1, 1, 2, 3, 4])
        self.destroyed = False

    def update(self, delta_time: float = 1/60):
       if not self.destroyed:  
            self.center_x += self.change_x
            if self.left < 120:
                self.change_x = abs(self.change_x) 
            elif self.right > WIDTH - 120:
                self.change_x = -abs(self.change_x) 

    def shoot(self, enemy_lasers: arcade.SpriteList):
        if not self.destroyed: 
            laser = EnemyLaser(center_x=self.center_x, center_y=self.center_y)
            enemy_lasers.append(laser)

class EnemyLaser(arcade.Sprite):
    def __init__(self, scale=0.08, speed=-5, center_x=0, center_y=0):
        super().__init__("assets/imgScreen/laserRay.png", scale, center_x, center_y)
        self.change_y = speed 

    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.center_y < 0 or self.center_y > HEIGHT:
            self.remove_from_sprite_lists()

class Level2GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.space = arcade.load_texture("assets/imgScreen/gamescreen.png")
        self.sound = arcade.load_sound("audio/level2.mp3")
        self.level2Sound = arcade.play_sound(self.sound, volume=0.2)
        self.sprite_list = arcade.SpriteList()
        self.enemies = arcade.SpriteList()
        self.laserRay = arcade.SpriteList()
        self.destroyed_enemies = arcade.SpriteList()
        self.enemy_lasers = arcade.SpriteList()
        self.player = Player(
            center_x=WIDTH // 4.5,
            center_y=HEIGHT // 4.5,
            scale=0.4
        )
        self.sprite_list.append(self.player)
        self.spawn_enemies()
        self.setup_controller()
    def setup_controller(self):
        if self.player.controller:
            self.player.controller.push_handlers(self)
            print("Control configurado en la vista del juego")


    def spawn_enemies(self):
        num_enemies = random.randint(10, 20)  
        for _ in range(num_enemies):
            x_pos = random.randint(50, WIDTH - 50)
            y_pos = random.randint(400, HEIGHT - 100)  
            enemy = Enemy(center_x=x_pos, center_y=y_pos, scale=0.15)
            self.enemies.append(enemy)

    def on_update(self, delta_time):
        self.sprite_list.update(delta_time)
        self.enemies.update(delta_time)
        self.laserRay.update(delta_time)
        self.destroyed_enemies.update(delta_time)
        self.enemy_lasers.update(delta_time)

       
        for laser in self.laserRay:
            laser.check_enemies(self.enemies,self.destroyed_enemies, self.player)

        for enemy in self.enemies:
            if random.random() < 0.01: 
                enemy.shoot(self.enemy_lasers)

        hits = arcade.check_for_collision_with_list(self.player, self.enemy_lasers)
        if hits:
            for h in hits:
                h.remove_from_sprite_lists()
            self.player.lives -= 1
            print(f"Vidas restantes: {self.player.lives}")
            if self.player.lives <= 0:
                screenGO = gameOverScreen.GameOverView()
                arcade.stop_sound(self.level2Sound)
                self.window.show_view(screenGO)
        if len(self.enemies) == 0:
            level3 = Level3.Level3GameView()
            arcade.stop_sound(self.level2Sound)
            self.window.show_view(level3)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.space, arcade.LRBT(0, WIDTH, 0, HEIGHT))
        self.sprite_list.draw()
        self.enemies.draw()
        self.laserRay.draw()
        self.enemy_lasers.draw()
        self.destroyed_enemies.draw()
       

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
            self.player.shoot(self.laserRay)

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


