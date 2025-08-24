import arcade
import random
import gameOverScreen
import Level3

WIDTH = 1280
HEIGHT = 720
TITLE = "hola arcade"
MOVEMENT_SPEED = 5


class Player(arcade.Sprite):
    def __init__(self, scale=0, center_x=0, center_y=0):
        super().__init__(
            "assets/imgScreen/navecita.png",
            scale, center_x, center_y)
        self.score = 0
        self.lives = 3

    def update(self, delta_time: float = 1 / 60):
        self.center_x += self.change_x
        self.center_y += self.change_y
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

    def check_enemies(self, enemies: arcade.SpriteList, player: "Player"):
        for enemy in enemies:
            if (
                    abs(self.center_x - enemy.center_x) < 20 and
                    abs(self.center_y - enemy.center_y) < 20
            ):
                enemies.remove(enemy)
                self.remove_from_sprite_lists()  # la bala desaparece al chocar
                player.score += 10
                break  # rompe el bucle porque la bala ya murió

class Enemy(arcade.Sprite):
    def __init__(self, scale = 1, center_x = 0, center_y = 0):
        super().__init__(
            "assets/imgScreen/alien1.png",
            scale, center_x, center_y)
        self.change_x = random.choice([-3, -2, -1, 1, 2, 3, 4])

    def update(self, delta_time: float = 1/60):
       self.center_x += self.change_x
       if self.left < 120:
            self.change_x = abs(self.change_x) 
       elif self.right > WIDTH - 120:
            self.change_x = -abs(self.change_x)  

    def shoot(self, enemy_lasers: arcade.SpriteList):
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
        self.enemy_lasers = arcade.SpriteList()
        self.player = Player(
            center_x=WIDTH // 4.5,
            center_y=HEIGHT // 4.5,
            scale=0.4
        )
        self.sprite_list.append(self.player)
        self.spawn_enemies()

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
        self.enemy_lasers.update(delta_time)

       
        for laser in self.laserRay:
            laser.check_enemies(self.enemies, self.player)

        for enemy in self.enemies:
            if random.random() < 0.01: 
                enemy.shoot(self.enemy_lasers)

        hits = arcade.check_for_collision_with_list(self.player, self.enemy_lasers)
        if len(self.enemies) == 0:
            level3 = Level3.Level3GameView()
            arcade.stop_sound(self.level2Sound)
            self.window.show_view(level3)
        if hits:
            for h in hits:
                h.remove_from_sprite_lists()
            self.player.lives -= 1
            print(f"Vidas restantes: {self.player.lives}")
            if self.player.lives <= 0:
                screenGO = gameOverScreen.GameOverView()
                arcade.stop_sound(self.level2Sound)
                self.window.show_view(screenGO)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.space, arcade.LRBT(0, WIDTH, 0, HEIGHT))
        self.sprite_list.draw()
        self.enemies.draw()
        self.laserRay.draw()
        self.enemy_lasers.draw()
       

        arcade.draw_text(
            f"Score: {self.player.score}",
            20,
            HEIGHT - 40,
            arcade.color.AERO_BLUE,
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


