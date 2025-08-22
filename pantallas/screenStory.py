import arcade

WIDTH = 1280
HEIGHT = 720
TITLE = "Screen Manager with Arcade"

class Story(arcade.Sprite):
    def __init__(self, scale=20, center_x=0, center_y=0):
        super().__init__("/Users/leonardocarrillo/1erParcialSW/Space_War-1er_Parcial_infograf-a/assets/imgScreen/story.png", scale, center_x, center_y)
        self.change_y = 0.1 

    def update(self, delta_time: float = 1/60):
        self.center_y += self.change_y
        if self.bottom > HEIGHT:
            self.top = 0  


class ScreenStoryView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture("/Users/leonardocarrillo/1erParcialSW/Space_War-1er_Parcial_infograf-a/assets/imgScreen/screen2.png")
        
        self.sound = arcade.load_sound("/Users/leonardocarrillo/1erParcialSW/Space_War-1er_Parcial_infograf-a/audio/8-bit-heaven-26287.mp3")

       
        self.player = Story(
            center_x=WIDTH // 2,  
            center_y=0,  
            scale=1.2
        )
        
        self.sprite_list = arcade.SpriteList()
        self.sprite_list.append(self.player)
        
        
        arcade.play_sound(self.sound, volume=0.2)
        
    def on_update(self, delta_time):
        """Actualizar la posición de los sprites"""
        self.sprite_list.update(delta_time)
        
    def on_draw(self):
        """Render the screen"""
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