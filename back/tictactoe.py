#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 18:09:47 2022

@author: heritianadanielandriasolofo
"""


class TicTacToe:
    def __init__(self) -> None:
        """Generate a Tic Tac Toe Game environment"""
        self.val = 1
        self.board = [[0] * 3 for _ in range(3)]
        self.number_of_empty = 9
        self.color = [0] * 8
        self.end = False
        self.winner = None
        self.actions = {
            0: (0, 0),
            1: (0, 1),
            2: (0, 2),
            3: (1, 0),
            4: (1, 1),
            5: (1, 2),
            6: (2, 0),
            7: (2, 1),
            8: (2, 2),
        }
        self.num_actions = 9

    def whose_turn(self):
        """Ask the environment the index of current player

        Returns:
            int: index of current player
        """
        return 0 if self.val == 1 else 1

    def get_reward(self, row, col):
        """Check wether the game is ended if current player play at the given position and return the respected reward.

        Args:
            row (int): row where player plays
            col (int): column where player plays

        Returns:
            int: reward obtain by playing at the given position
        """
        horizontal = (
            abs(self.board[row][0] + self.board[row][1] + self.board[row][2]) == 3
        )
        vertical = (
            abs(self.board[0][col] + self.board[1][col] + self.board[2][col]) == 3
        )
        diagonal = abs(self.board[0][0] + self.board[1][1] + self.board[2][2]) == 3
        antidiagonal = abs(self.board[0][2] + self.board[1][1] + self.board[2][0]) == 3

        reward = 0
        if self.number_of_empty == 0:
            self.end = True
            self.winner = None
        if horizontal:
            self.color[row] = self.val
            self.end = True
            self.winner = self.whose_turn()
            reward += 1
        if vertical:
            self.color[3 + col] = self.val
            self.end = True
            self.winner = self.whose_turn()
            reward += 1
        if diagonal:
            self.color[6] = self.val
            self.end = True
            self.winner = self.whose_turn()
            reward += 1
        if antidiagonal:
            self.color[7] = self.val
            self.end = True
            self.winner = self.whose_turn()
            reward += 1
        return reward

    def play(self, row, col):
        """Current player plays at the given row and column.

        Args:
            row (int): row where player want to play
            col (int): column where player want to play

        Returns:
            tuple[bool, int]: indication wether player was able to play at the given position, reward obtain by trying to play on the position
        """
        if self.end:
            return False, -sum(self.color)
        if not self.board[row][col] == 0:
            return False, -1  # penalize on typing on filled slot

        self.board[row][col] = self.val
        self.number_of_empty -= 1
        reward = self.get_reward(row, col)
        # switch player
        self.val *= -1
        return True, reward

    @property
    def hashed_state(self):
        """generate a hashed string for current state.

        Returns:
            str : hash for current state
        """
        return "".join("".join(map(lambda x: str(x % 3), row)) for row in self.board)

    def reset(self):
        """Reset environement:
        - Set hand to plalyer 1
        - Clear and uncolor the board

        Returns:
            str : empty state
        """
        self.val = 1
        self.board = [[0] * 3 for _ in range(3)]
        self.number_of_empty = 9
        self.color = [0] * 8
        self.end = False
        self.winner = None
        return self.hashed_state

    def step(self, action):
        """Make a step in the environement by performing an action.
        Actions are represented in a index form (from 0 to 8), where
        row 0, col 0 : action 0
        row 0, col 1 : action 1
        row 0, col 2 : action 2
        row 1, col 0 : action 3
        ...
        row 2, col 2 : action 8

        Args:
            action (int): index of the action to perform.


        Returns:
            tuple[str, int, bool, bool]: hashed of next state, reward from the action, indication if the game is done, indication if the player will be switched
        """
        switch, reward = self.play(*self.actions[action])
        return self.hashed_state, reward, self.end, switch
