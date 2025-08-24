import arcade
from game.settings import WIDTH, HEIGHT, TITLE
from game.views.game_view import GameView

def main():
    window = arcade.Window(WIDTH, HEIGHT, TITLE)
    game = GameView()
    window.show_view(game)
    arcade.run()

if __name__ == "__main__":
    main()
