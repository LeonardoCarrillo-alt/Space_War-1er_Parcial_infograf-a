import arcade

WIDTH = 1280
HEIGHT = 720
TITLE = "You Win!!!!!!!!"

class ScreenStoryView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture("/Users/leonardocarrillo/1erParcialSW/Space_War-1er_Parcial_infograf-a/assets/imgScreen/Win.png")
        
        self.sound = arcade.load_sound("/Users/leonardocarrillo/1erParcialSW/Space_War-1er_Parcial_infograf-a/audio/8bit-ME_Victory01.mp3")
        
        self.sprite_list = arcade.SpriteList()
        
        
        arcade.play_sound(self.sound, volume=0.2)
        
    def on_update(self, delta_time):
        self.sprite_list.update(delta_time)
        
    def on_draw(self):
        self.clear()
        
        arcade.draw_texture_rect(self.background, arcade.LRBT(0, WIDTH, 0, HEIGHT))
       
        self.sprite_list.draw()


def main():
    window = arcade.Window(WIDTH, HEIGHT, TITLE)
    screen_view = ScreenStoryView()
    window.show_view(screen_view)
    arcade.run()

if __name__ == "__main__":
    main()