import arcade
from game.views.game_view import GameView
from game.settings import WIDTH, HEIGHT

class DifficultyView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.DARK_BLUE

    def on_draw(self):
        self.clear()
        arcade.draw_text("Selecciona dificultad:",
                         WIDTH//2, HEIGHT//2 + 100, arcade.color.WHITE, 30, anchor_x="center")
        arcade.draw_text("[1] Fácil", WIDTH//2, HEIGHT//2 + 40, arcade.color.GREEN, 25, anchor_x="center")
        arcade.draw_text("[2] Normal", WIDTH//2, HEIGHT//2, arcade.color.YELLOW, 25, anchor_x="center")
        arcade.draw_text("[3] Difícil", WIDTH//2, HEIGHT//2 - 40, arcade.color.RED, 25, anchor_x="center")

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.KEY_1:
            self.start_game("facil")
        elif symbol == arcade.key.KEY_2:
            self.start_game("normal")
        elif symbol == arcade.key.KEY_3:
            self.start_game("dificil")

    def start_game(self, dificultad: str):
        # Aquí puedes pasar dificultad como parámetro al GameView si lo necesitas
        game_view = GameView()
        game_view.difficulty = dificultad
        self.window.show_view(game_view)
