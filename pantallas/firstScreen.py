import arcade
import screenStory
WIDTH = 1280
HEIGHT = 720
TITLE = "Screen1 - Space War"


class ScreenView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture("assets/imgScreen/screen1.png")
        self.sound = arcade.load_sound("audio/game-8-bit-on-278083.wav")
        
        self.playSound = arcade.play_sound(self.sound, volume=0.2)
        
    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background, arcade.LRBT(0, WIDTH, 0, HEIGHT))
     
    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.SPACE:
            screen2 = screenStory.ScreenStoryView()
            arcade.stop_sound(self.playSound)
            self.window.show_view(screen2)


def main():
    window = arcade.Window(WIDTH, HEIGHT, TITLE)
    screen_view = ScreenView()
    window.show_view(screen_view)
    arcade.run()

if __name__ == "__main__":
    main()