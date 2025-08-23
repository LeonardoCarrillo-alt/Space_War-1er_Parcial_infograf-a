import arcade
import random

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

    def shoot(self, laser: arcade.SpriteList):
        laser.append(LaserRay(center_x=self.center_x, center_y=self.center_y))

class LaserRay(arcade.Sprite):
    def __init__(self, scale= 0.1, speed=10, center_x=0, center_y=0):
        super().__init__("assets/imgScreen/laserRay.png", scale, center_x, center_y)
        self.change_y = speed

    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.center_x > WIDTH or self.center_x < 0 or self.center_y > HEIGHT:
            self.remove_from_sprite_lists()  # auto eliminacion

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

        if self.center_x < -20:
            self.center_x = WIDTH + 20
        elif self.center_x > WIDTH + 20:
            self.center_x = -20

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

class KeyboardMovementView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.BLACK
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
        num_enemies = random.randint(10, 20)  # entre 10 y 15
        for _ in range(num_enemies):
            x_pos = random.randint(50, WIDTH - 50)
            y_pos = random.randint(400, HEIGHT - 100)  # aparecen en la parte alta
            enemy = Enemy(center_x=x_pos, center_y=y_pos, scale=0.15)
            self.enemies.append(enemy)

    def on_update(self, delta_time):
        self.sprite_list.update(delta_time)
        self.enemies.update(delta_time)
        self.laserRay.update(delta_time)
        self.enemy_lasers.update(delta_time)

        # Colisiones de mis balas con enemigos
        for laser in self.laserRay:
            laser.check_enemies(self.enemies, self.player)

        # Los enemigos disparan aleatoriamente
        for enemy in self.enemies:
            if random.random() < 0.01:  # probabilidad de disparar
                enemy.shoot(self.enemy_lasers)

        # Colisiones de balas enemigas con el jugador
        hits = arcade.check_for_collision_with_list(self.player, self.enemy_lasers)
        if hits:
            for h in hits:
                h.remove_from_sprite_lists()
            self.player.lives -= 1
            print(f"Vidas restantes: {self.player.lives}")
            if self.player.lives <= 0:
                print("Game Over")
                arcade.close_window()

    def on_draw(self):
        self.clear()
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


def main():
    window = arcade.Window(WIDTH, HEIGHT, TITLE)
    game = KeyboardMovementView()
    window.show_view(game)
    arcade.run()


if __name__ == "__main__":
    main()