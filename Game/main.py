import arcade
import firstScreen
import screenStory

WIDTH = 1280
HEIGHT = 720
TITLE = "Space War - Game"

class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, TITLE)
        
        # Crear las vistas
        self.screen_view = firstScreen.ScreenView()
        self.story_view = screenStory.ScreenStory()
        
        # Mostrar la primera pantalla
        self.show_view(self.screen_view)

def main():
    window = GameWindow()
    arcade.run()

if __name__ == "__main__":
    main()