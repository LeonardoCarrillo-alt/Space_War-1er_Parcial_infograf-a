import arcade
from game.views.story_view import StoryView
from game.settings import WIDTH, HEIGHT

class StartView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture("img/screen1.png")
        #self.sound = arcade.load_sound("audio/game-8-bit-on-278083.wav")
        #self.music = arcade.play_sound(self.sound, volume=0.2)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background, arcade.LRBT(0, WIDTH, 0, HEIGHT))

        arcade.draw_text("Presiona [ESPACIO] para continuar",
                         WIDTH//2, 50, arcade.color.WHITE, 20, anchor_x="center")

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.SPACE:
            #self.sound.stop()
            story_view = StoryView()
            self.window.show_view(story_view)
