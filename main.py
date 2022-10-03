from back.tictactoe import TicTacToe
from back.player_module import QAgent
from back.utils import read_json, return_probabilities

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
        self._cpu = [False, False]
        self._agents = [None, None]

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

    def play_update_screen(self, row: int, col: int):
        """Update screen after playing at a given position

        Args:
            row (int): row position where current player plays
            col (int): col position where current player plays
        """
        symb = self.symbols[0] if self.hand_index == -1 else self.symbols[1]
        self.ids[f"bt{row}{col}"].text = symb
        hand = self.players_name[self.hand]
        self.ids.textup.text = f"{hand}'s turn"

    def update_empty_label(self):
        """Update the number of empty label in the screen"""
        num_empty = self.game.number_of_empty
        self.ids.numEmpty.text = f"Empty : {num_empty}" if num_empty else "Game over"
        color = num_empty / 9
        self.ids.numEmpty.background_color = (color, color, color, 1)
        self.ids.numEmpty.color = (1 - color, 0, color * (1 - color), 1)

    def update_save_agent(self, state, action, reward, done, hand):
        next_state = self.game.hashed_state
        self._agents[hand].update(state, action, next_state, reward, done)
        if done:
            path_qfunction = f"src/qvalue/qvalue_player{hand+1}.json"
            path_policy = f"src/policy/expert_player{hand+1}.json"
            self._agents[hand].save_qfunction(path_qfunction)
            self._agents[hand].generate_policy("greedy", path_policy)

    def play(self, row: int, col: int):
        """Let current player to play at the given position if the move is allowed.

        Args:
            row (int): row where player want to play
            col (int): column where player want to play
        """
        hand = self.hand
        state = self.game.hashed_state
        valid_move, reward = self.game.play(row, col)
        done = self.game_over
        action = 3 * row + col
        if isinstance(self._agents[hand], QAgent):
            self.update_save_agent(state, action, reward, done, hand)

        if valid_move:
            self.play_update_screen(row, col)
            self.update_empty_label()

        if done:
            if self.winner is not None:
                winner = self.players_name[self.winner]
                for i, val in enumerate(self.game.color):
                    if not val == 0:
                        self.color_board(i)
                self.ids.textup.text = f"{winner} wins!"
            else:
                winner = None
                self.ids.textup.text = "Draw!"

            # self.add_stats(winner=winner)
        elif self._cpu[self.hand]:
            self.auto_play()

    def auto_play(self):
        """Ask cpu agent to play"""

        state = self.game.hashed_state
        player = self._agents[self.hand]
        if isinstance(player, dict):  # policy
            p = return_probabilities(
                state, np.zeros(self.game.num_actions), kind="random"
            )
            probs = player.get(state, p)
            action = np.random.choice(self.game.num_actions, p=probs)
        else:  # Qagent
            action = player.act(state=state, eval=True)
        row, col = self.game.actions[action]
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
        new_name = self.ids[f"player{player_n}"].text.strip()[:max_name_length]

        self.ids[f"player{player_n}"].text = new_name
        if new_name:
            self.players_name[int(player_n) - 1] = new_name
        else:
            self.players_name[int(player_n) - 1] = f"player{player_n}"

        if new_name == "train expert":
            self._cpu[player_n - 1] = True
            qfunction = read_json(
                f"./src/qvalue/qvalue_player{player_n}.json", return_as_array=True
            )
            self._agents[player_n - 1] = QAgent(
                num_actions=9,
                gamma=0.999,
                learning_rate=0.01,
                epsilon=1,
                qfunction=qfunction,
            )
            if self.hand == player_n - 1:
                self.auto_play()

        elif (
            "cpu" == new_name[:3].lower()
            and len(new_name) == 4
            and new_name[-1] in "1234"
        ):
            self._cpu[player_n - 1] = True
            lvl = new_name[-1]

            if lvl in "0123":  # policy
                level = {0: "easy", 1: "medium", 2: "hard", 3: "expert"}[int(lvl)]
                player = "" if level == "easy" else f"_player{player_n}"
                self._agents[player_n - 1] = read_json(
                    f"./src/policy/{level}{player}.json"
                )

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
