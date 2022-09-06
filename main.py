from back.tictactoe import TicTacToe

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.core.window import Window

Builder.load_file("./front/main.kv")
Window.size = (500, 700)


class TicTacToeLayout(Widget):
    def __init__(self, ** kwargs):
        super().__init__(**kwargs)
        self.game = TicTacToe()
        self.ids.textup.text = f"Set names and start."
        self.symbols = ["X", "O"]

    def play(self, row, col):
        if self.game.play(row, col):
            exec(
                f"self.ids.bt{row}{col}.text = self.symbols[0] if self.game.val == -1 else self.symbols[1]")
            self.ids.textup.text = f"{self.game.whose_turn()}'s turn"
        if self.game.end:
            self.ids.textup.text = f"{self.game.winner} wins" if self.game.winner is not None else "Draw"

    def entered_name(self, player_n):
        exec(
            f"self.game.setplayers_name(self.ids.player{player_n}.text if self.ids.player{player_n}.text != '' else 'player{player_n}', {player_n})")
        if not self.game.end:
            self.ids.textup.text = f"{self.game.whose_turn()}'s turn"

    def entered_symbol(self, player_n):
        for row in range(3):
            for col in range(3):
                exec(
                    f"if self.ids.bt{row}{col}.text == self.symbols[player_n - 1]: self.ids.bt{row}{col}.text = self.ids.symbol{player_n}.text if self.ids.symbol{player_n}.text != '' else 'X' if player_n == 1 else 'O';")
        exec(
            f"self.symbols[player_n - 1] = self.ids.symbol{player_n}.text if self.ids.symbol{player_n}.text != '' else 'X' if player_n == 1 else 'O'")


class TicTacToeAPP(App):
    def build(self):
        return TicTacToeLayout()


if __name__ == "__main__":

    TicTacToeAPP().run()
