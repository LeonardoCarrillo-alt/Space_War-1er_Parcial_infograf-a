import arcade
from game.views.difficulty_view import DifficultyView
from game.settings import WIDTH, HEIGHT

class Story(arcade.Sprite):
    def __init__(self, scale=1.2, center_x=0, center_y=0):
        super().__init__("img/screen1.png", scale, center_x, center_y)
        self.change_y = 0.5

    def update(self, delta_time: float = 1/60):
        self.center_y += self.change_y
        if self.bottom > HEIGHT:
            self.top = 0

class StoryView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture("img/screen2.png")
        #self.sound = arcade.load_sound("audio/8-bit-heaven-26287.mp3")
        #arcade.play_sound(self.sound, volume=0.2)

        self.story_sprite = Story(center_x=WIDTH//2, center_y=0)
        self.story_list = arcade.SpriteList()
        self.story_list.append(self.story_sprite)

    def on_update(self, delta_time):
        self.story_list.update(delta_time)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background, arcade.LRBT(0, WIDTH, 0, HEIGHT))
        self.story_list.draw()

        arcade.draw_text("Presiona [ENTER] para elegir dificultad",
                         WIDTH//2, 50, arcade.color.WHITE, 20, anchor_x="center")

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ENTER:
            difficulty_view = DifficultyView()
            self.window.show_view(difficulty_view)
