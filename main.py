from back.tictactoe import TicTacToe

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.core.window import Window

Builder.load_file("./front/main.kv")
# Window.size = (500, 700)


class TicTacToeLayout(Widget):
    def __init__(self, ** kwargs):
        super().__init__(**kwargs)
        self.game = TicTacToe()
        self.ids.textup.text = "Set names"
        self.symbols = ["X", "O"]
        self.players_name = ["player1", "player2"]

    def play(self, row, col):
        if self.game.play(row, col):
            symb = self.symbols[0] if self.game.val == -1 else self.symbols[1]
            self.ids[f"bt{row}{col}"].text = symb
            hand = self.players_name[self.game.whose_turn()]
            self.ids.textup.text = f"{hand}'s turn"
        self.ids.numEmpty.text = f"Empty : {self.game.number_of_empty}"
        if self.game.end:
            winner = self.players_name[self.game.winner] if self.game.winner is not None else None
            self.ids.textup.text = f"{winner} wins!" if winner is not None else "Draw!"

    def entered_name(self, player_n):
        new_name = self.ids[f"player{player_n}"].text
        self.players_name[int(
            player_n) - 1] = new_name if new_name != '' else f"player{player_n}"
        if not self.game.end:
            hand = self.players_name[self.game.whose_turn()]
            self.ids.textup.text = f"{hand}'s turn"

    def entered_symbol(self, player_n):
        new_symbol = self.ids[f"symbol{player_n}"].text
        player_val = 1 if player_n == 1 else -1
        for row in range(3):
            for col in range(3):
                if self.game.board[row][col] == player_val:
                    if new_symbol != '':
                        self.ids[f"bt{row}{col}"].text = new_symbol
                    else:
                        self.ids[f"bt{row}{col}"].text = 'X' if player_n == 1 else 'O'
        if new_symbol != '':
            self.symbols[player_n - 1] = new_symbol
        else:
            self.symbols[player_n - 1] = 'X' if player_n == 1 else 'O'

    def restart(self):
        for row in range(3):
            for col in range(3):
                self.ids[f"bt{row}{col}"].text = ''
        self.game = TicTacToe()
        self.ids.textup.text = "Start"
        self.ids.numEmpty.text = ''


class TicTacToeAPP(App):
    def build(self):
        return TicTacToeLayout()


if __name__ == "__main__":
    TicTacToeAPP().run()
