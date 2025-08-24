import arcade
import firstScreen

WIDTH = 1280
HEIGHT = 720
TITLE = "You Win!!!!!!!!"

class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture("assets/imgScreen/gameOver.png")
        
        self.sound = arcade.load_sound("audio/game-over-284367.mp3")
        
        self.sprite_list = arcade.SpriteList()
        
        
        self.playGO = arcade.play_sound(self.sound, volume=0.2)
        
    def on_update(self, delta_time):
        self.sprite_list.update(delta_time)
        
    def on_draw(self):
        self.clear()
        
        arcade.draw_texture_rect(self.background, arcade.LRBT(0, WIDTH, 0, HEIGHT))
       
        self.sprite_list.draw()

    def on_key_press(self, symbol: int, modifiers: int) :
        if symbol == arcade.key.ESCAPE:
            arcade.close_window()
        elif symbol == arcade.key.ENTER:
            screenWin = firstScreen.ScreenView()
            arcade.stop_sound(self.playGO)
            self.window.show_view(screenWin)
