import arcade 

WIDTH = 1280
HEIGHT = 720
TITLE = "Space War - Game"

class FirstScreen(arcade.View): 
    def on_show_view(self):
        self.firstscreen = arcade.load_texture("assets/imgScreen/screen1.png")
        self.sound1 = arcade.load_sound("audio/game-8-bit-on-278083.wav")
        arcade.play_sound(self.sound1, volume=0.2)
    
    def on_draw(self):
        self.clear()
        # FORMA CORRECTA 1: Usar draw_texture_rectangle
        arcade.draw_texture_rect(
           self.firstscreen, arcade.LRBT(0, WIDTH, 0, HEIGHT)
        )
    
    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.SPACE:
            self.sound1.stop()
            story_view = StoryScreen()
            self.window.show_view(story_view)

class StoryScreen(arcade.View):
    def on_show_view(self):
        self.storyscreen = arcade.load_texture("assets/imgScreen/screen2.png")
    
    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(
            self.storyscreen, arcade.LRBT(0, WIDTH, 0, HEIGHT)
        )

def main():
    window = arcade.Window(WIDTH, HEIGHT, TITLE)
    game = FirstScreen()
    window.show_view(game)
    arcade.run()

if __name__ == "__main__":
    main()