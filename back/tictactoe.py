#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 18:09:47 2022

@author: heritianadanielandriasolofo
"""


class TicTacToe:
    def __init__(self) -> None:
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
        return 0 if self.val == 1 else 1

    def get_reward(self, row, col):
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
            reward += 2
        if vertical:
            self.color[3 + col] = self.val
            self.end = True
            self.winner = self.whose_turn()
            reward += 2
        if diagonal:
            self.color[6] = self.val
            self.end = True
            self.winner = self.whose_turn()
            reward += 2
        if antidiagonal:
            self.color[7] = self.val
            self.end = True
            self.winner = self.whose_turn()
            reward += 2
        return reward

    def play(self, row, col):
        if self.end:
            return False, -5  # loose
        if not self.board[row][col] == 0:
            return False, -2  # penalize on typing on filled slot

        self.board[row][col] = self.val
        self.number_of_empty -= 1
        reward = self.get_reward(row, col)
        # switch player
        self.val *= -1
        return True, reward

    @property
    def hashed_state(self):
        return "".join("".join(map(lambda x: str(x % 3), row)) for row in self.board)

    def reset(self):
        self.val = 1
        self.board = [[0] * 3 for _ in range(3)]
        self.number_of_empty = 9
        self.color = [0] * 8
        self.end = False
        self.winner = None
        return "0" * 9  # hashed_state for empty

    def step(self, action):
        switch, reward = self.play(*self.actions[action])
        return self.hashed_state, reward, self.end, switch
