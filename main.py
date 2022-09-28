from back.tictactoe import TicTacToe
from back.utils import read_json_policy, return_probabilities

import numpy as np
from typing import *

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.widget import Widget

Builder.load_file("./front/main.kv")


class TicTacToeLayout(Widget):
    def __init__(self, **kwargs):
        """Tic Tac Toe main widget"""

        super().__init__(**kwargs)
        self.game = TicTacToe()
        self.ids.textup.text = "Set names (cpu1/cpu2/cpu3 for cpu)"
        self.symbols = ["X", "O"]
        self.players_name = ["player1", "player2"]
        self._policy = [None, None]
        self._cpu = [False, False]

    @property
    def game_over(self):
        return self.game.end

    @property
    def hand(self):
        return self.game.whose_turn()

    @property
    def hand_index(self):
        return self.game.val

    @property
    def winner(self):
        return self.game.winner

    def color_board(self, i: int):
        """Coloring the coresponding winning boxes to be green

        Args:
            i (int): index of winning boxes
        """
        color = (0, 1, 0, 1)  # Green
        if i < 3:  # row
            row = i
            for col in range(3):
                self.ids[f"bt{row}{col}"].background_color = color
        elif i < 6:  # col
            col = i - 3
            for row in range(3):
                self.ids[f"bt{row}{col}"].background_color = color
        elif i == 6:  # diag
            for row_col in range(3):
                self.ids[f"bt{row_col}{row_col}"].background_color = color
        elif i == 7:  # antidiag
            for row in range(3):
                self.ids[f"bt{row}{2-row}"].background_color = color

    def play(self, row: int, col: int):
        """Let current player to play at the given position if the move is allowed.

        Args:
            row (int): row where player want to play
            col (int): column where player want to play
        """
        if self.game.play(row, col)[0]:
            symb = self.symbols[0] if self.hand_index == -1 else self.symbols[1]
            self.ids[f"bt{row}{col}"].text = symb
            hand = self.players_name[self.hand]
            self.ids.textup.text = f"{hand}'s turn"

        num_empty = self.game.number_of_empty
        self.ids.numEmpty.text = f"Empty : {num_empty}" if num_empty else "Game over"
        color = num_empty / 9
        self.ids.numEmpty.background_color = (color, color, color, 1)
        self.ids.numEmpty.color = (1 - color, 0, color * (1 - color), 1)

        if self.game_over:
            if self.winner is not None:
                winner = self.players_name[self.winner]
                for i, val in enumerate(self.game.color):
                    if not val == 0:
                        self.color_board(i)
            else:
                winner = None
            self.ids.textup.text = f"{winner} wins!" if winner is not None else "Draw!"

            # self.add_stats(winner=winner)
        if self._cpu[self.hand] and not self.game_over:
            self.auto_play()

    def auto_play(self):
        """Ask cpu to play following its corresponding policy"""
        hash = self.game.hashed_state
        p = return_probabilities(hash, np.zeros(self.game.num_actions), kind="random")
        probs = self._policy[self.hand].get(hash, p)
        action = np.random.choice(self.game.num_actions, p=probs)
        row, col = self.game.actions[action]
        self.ids[f"bt{row}{col}"].background_color = (50 / 255, 164 / 255, 206 / 255, 1)
        self.play(row, col)

    def add_stats(self, winner: str):
        """Add statistic in the stats data.

        Args:
            winner (str, NoneType): the name of winner or None if it is a draw
        """
        with open("data/stats/stats.csv", "a") as stats:
            stats.write(f"{self.players_name[0]}, {self.players_name[1]}, {winner}\n")

    def entered_name(self, player_n: int):
        """Set player's name from the interface
        If player's name is part of `cpu` players, it will load the corresponding policy.

        Args:
            player_n (int): index (1 or 2) of player
        """
        max_name_length = 20
        new_name = self.ids[f"player{player_n}"].text[:max_name_length].replace(" ", "")
        name = new_name[:-1].lower()
        if name == "cpu":
            try:
                lvl = int(new_name[-1])
            except ValueError:
                lvl = None
        self.ids[f"player{player_n}"].text = new_name
        self.players_name[int(player_n) - 1] = (
            new_name if new_name != "" else f"player{player_n}"
        )
        if name == "cpu" and lvl in (1, 2, 3):
            level = {1: "easy", 2: "medium", 3: "hard"}[lvl]
            player = "" if level == "easy" else f"_player{player_n}"
            self._policy[player_n - 1] = read_json_policy(
                f"./back/json_agents/{level}{player}.json"
            )
            self._cpu[player_n - 1] = True
            if self.hand == player_n - 1:
                self.auto_play()
        else:
            self._cpu[player_n - 1] = False

        if not self.game_over:
            hand = self.players_name[self.hand]
            self.ids.textup.text = f"{hand}'s turn"

    def entered_symbol(self, player_n):
        """Edit all the symbols for corresponding player

        Args:
            player_n (int): index (1 or 2) of player
        """
        new_symbol = self.ids[f"symbol{player_n}"].text
        player_val = 1 if player_n == 1 else -1
        for row in range(3):
            for col in range(3):
                if self.game.board[row][col] == player_val:
                    if new_symbol != "":
                        self.ids[f"bt{row}{col}"].text = new_symbol
                    else:
                        self.ids[f"bt{row}{col}"].text = "X" if player_n == 1 else "O"
        if new_symbol != "":
            self.symbols[player_n - 1] = new_symbol
        else:
            self.symbols[player_n - 1] = "X" if player_n == 1 else "O"

    def restart(self):
        """Restart the game from the begining."""
        for row in range(3):
            for col in range(3):
                self.ids[f"bt{row}{col}"].text = ""
                self.ids[f"bt{row}{col}"].background_color = (1, 1, 1, 1)
        self.game.reset()
        self.ids.textup.text = "Start"
        self.ids.numEmpty.text = ""
        self.ids.numEmpty.background_color = (0, 0, 0, 1)
        if self._cpu[self.hand]:
            self.auto_play()


class TicTacToeAPP(MDApp):
    def build(self):
        return TicTacToeLayout()


if __name__ == "__main__":
    TicTacToeAPP().run()
