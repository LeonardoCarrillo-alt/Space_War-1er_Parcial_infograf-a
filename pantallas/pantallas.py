import arcade
import os

WIDTH = 1280
HEIGHT = 720
TITLE = "Screen Manager with Arcade"

class Screens:
    def __init__(self):
        # List of screen images
        self.images = [
            arcade.load_texture("imgScreen/screen1.png"),
            arcade.load_texture("imgScreen/screen2.png"),
            arcade.load_texture("imgScreen/gamescreen.png"),
            arcade.load_texture("imgScreen/Win.png"),
            arcade.load_texture("imgScreen/gameOver.png"),   
        ]
        self.current_screen_index = 0
        
    def next_screen(self):
        """Move to the next screen"""
        self.current_screen_index = (self.current_screen_index + 1) % len(self.images)
        
    def set_screen(self, index):
        """Set a specific screen by index"""
        if 0 <= index < len(self.images):
            self.current_screen_index = index
            
    def get_current_texture(self):
        """Get the current screen texture"""
        return self.images[self.current_screen_index]
    
    def draw(self):
        """Draw the current screen"""
        arcade.draw_texture(
            WIDTH // 2, 
            HEIGHT // 2, 
            WIDTH, 
            HEIGHT, 
            self.get_current_texture()
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
            # Change to next screen
            self.screens.next_screen()
        elif symbol == arcade.key.ESCAPE:
            # Exit the game
            arcade.close_window()
        elif symbol == arcade.key.KEY_1:
            # Go directly to screen 1
            self.screens.set_screen(0)
        elif symbol == arcade.key.KEY_2:
            # Go directly to screen 2
            self.screens.set_screen(1)
        elif symbol == arcade.key.KEY_3:
            # Go directly to screen 3
            self.screens.set_screen(2)
        elif symbol == arcade.key.KEY_4:
            # Go directly to screen 4
            self.screens.set_screen(3)
        elif symbol == arcade.key.KEY_5:
            # Go directly to screen 5
            self.screens.set_screen(4)


def main():
    window = arcade.Window(WIDTH, HEIGHT, TITLE)
    screen_view = ScreenView()
    window.show_view(screen_view)
    arcade.run()

if __name__ == "__main__":
    main()