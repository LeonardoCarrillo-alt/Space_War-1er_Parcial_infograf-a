import arcade
import random

WIDTH = 1280
HEIGHT = 720
TITLE = "Space War - Nivel 1"
MOVEMENT_SPEED = 5
DEAD_ZONE = 0.2  # Zona muerta para evitar drift del joystick

class Player(arcade.Sprite):
    def __init__(self, scale=0, center_x=0, center_y=0):
        super().__init__(
            "/Users/leonardocarrillo/1erParcialSW/Space_War-1er_Parcial_infograf-a/assets/imgScreen/navecita.png",
            scale, center_x, center_y)
        self.score = 0
        self.controller = None
        self.game_view = None  # Referencia a la vista del juego
        
        # Conectar con el control
        controllers = arcade.get_game_controllers()
        print(f"Encontrados {len(controllers)} controles!")
        
        if controllers:
            self.controller = controllers[0]
            self.controller.open()
            # NO registrar manejadores aquí, se registrarán en la vista principal
            print("Conectado a un control")

    def update(self, delta_time: float = 1 / 60):
        # Movimiento solo horizontal con límites de pantalla
        self.center_x += self.change_x
        
        # Mantener dentro de los límites horizontales de la pantalla
        if self.left < 0:
            self.left = 0
        if self.right > WIDTH:
            self.right = WIDTH

    def shoot(self, laser_list: arcade.SpriteList):
        # Crear nuevo láser en la posición actual de la nave
        new_laser = LaserRay(center_x=self.center_x, center_y=self.center_y)
        laser_list.append(new_laser)
        print("¡Disparo realizado!")


class LaserRay(arcade.Sprite):
    def __init__(self, scale=0.1, speed=10, center_x=0, center_y=0):
        super().__init__("/Users/leonardocarrillo/1erParcialSW/Space_War-1er_Parcial_infograf-a/assets/imgScreen/laserRay.png", scale, center_x, center_y)
        self.change_y = speed
        # Posicionar el láser justo encima de la nave
        self.bottom = center_y + 30  # Ajusta este valor según la altura de tu nave

    def update(self, delta_time):
        self.center_y += self.change_y
        
        # Eliminar si sale de la pantalla por arriba
        if self.bottom > HEIGHT:
            self.remove_from_sprite_lists()

    def check_enemies(self, enemies: arcade.SpriteList, player: "Player"):
        # Usar detección de colisiones de Arcade en lugar de verificación manual
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
            "/Users/leonardocarrillo/1erParcialSW/Space_War-1er_Parcial_infograf-a/assets/imgScreen/alien1.png",
            scale, center_x, center_y)
        self.change_x = random.choice([-3, -2, -1, 1, 2, 3])  # Velocidades más variadas
        
    def update(self, delta_time: float=1/60):
        self.center_x += self.change_x

        # Rebote en los bordes
        if self.left < 20:
            self.change_x = abs(self.change_x)  # Cambiar a dirección positiva
        elif self.right > WIDTH - 20:
            self.change_x = -abs(self.change_x)  # Cambiar a dirección negativa


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.BLACK
        self.sprite_list = arcade.SpriteList()
        self.enemies = arcade.SpriteList()
        self.lasers = arcade.SpriteList()
        self.player = Player(
            center_x=WIDTH // 2,
            center_y=100,
            scale=0.4
        )
        self.player.game_view = self  # Establecer referencia a la vista del juego
        self.sprite_list.append(self.player)
        self.spawn_enemies()
        
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

        # Verificar colisiones de todos los láseres con enemigos
        for laser in self.lasers:
            laser.check_enemies(self.enemies, self.player)
            
        # Si no quedan enemigos, generar nuevos
        if len(self.enemies) == 0:
            self.spawn_enemies()

    def on_draw(self):
        self.clear()
        self.sprite_list.draw()
        self.enemies.draw()
        self.lasers.draw()
        
        # Mostrar puntuación
        arcade.draw_text(
            f"Score: {self.player.score}",
            20,
            HEIGHT - 40,
            arcade.color.AERO_BLUE,
            font_size=25)
            
        # Mostrar instrucciones
        arcade.draw_text(
            self.instruction_text,
            20,
            HEIGHT - 80,
            arcade.color.LIGHT_GRAY,
            font_size=16)
            
        # Mostrar último botón presionado (para debug)
        arcade.draw_text(
            f"Último botón: {self.last_button_pressed}",
            20,
            HEIGHT - 120,
            arcade.color.YELLOW,
            font_size=16)

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
            
    # Manejadores de eventos del control - REGISTRADOS EN LA VISTA PRINCIPAL
    def on_joybutton_press(self, controller, button):
        print(f"Botón presionado en la vista: {button}")
        self.last_button_pressed = button
        
        # Mapeo de botones comunes de PlayStation
        if button == "x":  # Botón X en PlayStation
            self.player.shoot(self.lasers)
            print("Disparando con botón X del control")
        elif button == "a":  # Algunos controles pueden usar nomenclatura diferente
            self.player.shoot(self.lasers)
            print("Disparando con botón A del control")
        elif button == "0":  # A veces los botones se identifican por números
            self.player.shoot(self.lasers)
            print("Disparando con botón 0 del control")
            
        # Probar todos los botones posibles
        self.player.shoot(self.lasers)  # Disparar con cualquier botón para pruebas
        
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


def main():
    window = arcade.Window(WIDTH, HEIGHT, TITLE)
    game = GameView()
    window.show_view(game)
    arcade.run()


if __name__ == "__main__":
    main()