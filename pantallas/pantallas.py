import arcade
import os

WIDTH = 1280
HEIGHT = 720
TITLE = "Screen Manager with Arcade"

class Screens:
    def __init__(self):
        # Lista de rutas de imágenes
        self.image_paths = [
            "imgScreen/screen1.png",
            "imgScreen/screen2.png", 
            "imgScreen/gamescreen.png",
            "imgScreen/Win.png",
            "imgScreen/gameOver.png",   
        ]
        self.images = []
        self.current_screen_index = 0
        self.load_images()
        
    def load_images(self):
        """Cargar todas las imágenes con manejo de errores"""
        for i, path in enumerate(self.image_paths):
            try:
                # Verificar si el archivo existe
                if os.path.exists(path):
                    self.images.append(arcade.load_texture(path))
                    print(f"Imagen cargada: {path}")
                else:
                    print(f"Advertencia: No se encontró {path}")
                    # Crear una imagen de placeholder si no existe
                    self.create_placeholder_image(i)
            except Exception as e:
                print(f"Error cargando {path}: {e}")
                self.create_placeholder_image(i)
    
    def create_placeholder_image(self, index):
        """Crear una imagen de placeholder cuando falta una imagen"""
        # Crear un sprite simple como placeholder
        colors = [arcade.color.RED, arcade.color.BLUE, arcade.color.GREEN, 
                 arcade.color.YELLOW, arcade.color.PURPLE]
        color = colors[index % len(colors)]
        
        # Crear una textura de color sólido
        from arcade import create_rectangle_filled
        shape = create_rectangle_filled(WIDTH//2, HEIGHT//2, WIDTH, HEIGHT, color)
        self.images.append(shape.texture)
        
    def next_screen(self):
        """Move to the next screen"""
        if self.images:
            self.current_screen_index = (self.current_screen_index + 1) % len(self.images)
        
    def set_screen(self, index):
        """Set a specific screen by index"""
        if self.images and 0 <= index < len(self.images):
            self.current_screen_index = index
            
    def get_current_texture(self):
        """Get the current screen texture"""
        if self.images:
            return self.images[self.current_screen_index]
        return None
    
    def draw(self):
        """Draw the current screen"""
        texture = self.get_current_texture()
        if texture:
            arcade.draw_texture_rectangle(
                WIDTH // 2, 
                HEIGHT // 2, 
                WIDTH, 
                HEIGHT, 
                texture
            )


class ScreenView(arcade.View):
    def __init__(self):
        super().__init__()
        self.screens = Screens()
        
    def on_draw(self):
        """Render the screen"""
        self.clear()
        self.screens.draw()
        
        # Draw instructions
        arcade.draw_text(
            "Press SPACE to change screens | ESC to exit",
            WIDTH // 2,
            30,
            arcade.color.WHITE,
            20,
            align="center",
            anchor_x="center"
        )
        
        # Draw current screen indicator
        if self.screens.images:
            arcade.draw_text(
                f"Screen {self.screens.current_screen_index + 1} of {len(self.screens.images)}",
                WIDTH // 2,
                HEIGHT - 30,
                arcade.color.WHITE,
                24,
                align="center",
                anchor_x="center"
            )
        
    def on_key_press(self, symbol, modifiers):
        """Handle key presses"""
        if symbol == arcade.key.SPACE:
            self.screens.next_screen()
        elif symbol == arcade.key.ESCAPE:
            arcade.close_window()
        elif symbol == arcade.key.KEY_1:
            self.screens.set_screen(0)
        elif symbol == arcade.key.KEY_2:
            self.screens.set_screen(1)
        elif symbol == arcade.key.KEY_3:
            self.screens.set_screen(2)
        elif symbol == arcade.key.KEY_4:
            self.screens.set_screen(3)
        elif symbol == arcade.key.KEY_5:
            self.screens.set_screen(4)


def main():
    # Verificar si la carpeta existe
    if not os.path.exists("imgScreen"):
        print("Creando carpeta imgScreen...")
        os.makedirs("imgScreen")
        print("Por favor, coloca tus imágenes en la carpeta 'imgScreen'")
        print("Nombres requeridos: screen1.png, screen2.png, gamescreen.png, Win.png, gameOver.png")
    
    window = arcade.Window(WIDTH, HEIGHT, TITLE)
    screen_view = ScreenView()
    window.show_view(screen_view)
    arcade.run()

if __name__ == "__main__":
    main()