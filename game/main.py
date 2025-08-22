import arcade
from game.settings import WIDTH, HEIGHT, TITLE
from game.views.start_view import StartView

def main():
    window = arcade.Window(WIDTH, HEIGHT, TITLE)
    start_view = StartView()
    window.show_view(start_view)
    arcade.run()

if __name__ == "__main__":
    main()
