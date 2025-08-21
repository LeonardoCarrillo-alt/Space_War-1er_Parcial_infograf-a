import arcade

WIDTH = 1280
HEIGHT = 720
TITLE = "Screen Manager with Arcade"

class ScreenView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture("/Users/leonardocarrillo/1erParcialSW/Space_War-1er_Parcial_infograf-a/assets/imgScreen/screen1.png")
        
        # Cargar el sonido pero no reproducirlo aún
        self.sound = arcade.load_sound("/Users/leonardocarrillo/1erParcialSW/Space_War-1er_Parcial_infograf-a/audio/game-8-bit-on-278083.wav")
        
        arcade.play_sound(self.sound, volume=0.2)
        
    def on_draw(self):
        """Render the screen"""
        self.clear()
        arcade.draw_texture_rect(self.background, arcade.LRBT(0, WIDTH, 0, HEIGHT))

def main():
    window = arcade.Window(WIDTH, HEIGHT, TITLE)
    screen_view = ScreenView()
    window.show_view(screen_view)
    arcade.run()

if __name__ == "__main__":
    main()