#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 18:09:47 2022

@author: heritianadanielandriasolofo
"""


class TicTacToe:
    def __init__(self) -> None:
        self.val = 1
        self.board = [[0]*3 for _ in range(3)]
        self.number_of_empty = 9
        self.state = [0]*8
        self.end = False
        self.winner = None

    def whose_turn(self):
        return 0 if self.val == 1 else 1

    def get_reward(self, row, col):
        horizontal = abs(self.board[row][0] +
                         self.board[row][1] + self.board[row][2]) == 3
        vertical = abs(self.board[0][col] + self.board[1]
                       [col] + self.board[2][col]) == 3
        diagonal = abs(self.board[0][0] + self.board[1]
                       [1] + self.board[2][2]) == 3
        antidiagonal = abs(self.board[0][2] +
                           self.board[1][1] + self.board[2][0]) == 3

        reward = 0
        if self.number_of_empty == 0:
            self.end = True
            self.winner = None
        if horizontal:
            self.state[row] = self.val
            self.end = True
            self.winner = self.whose_turn()
            reward += 1
        if vertical:
            self.state[3+col] = self.val
            self.end = True
            self.winner = self.whose_turn()
            reward += 1
        if diagonal:
            self.state[6] = self.val
            self.end = True
            self.winner = self.whose_turn()
            reward += 1
        if antidiagonal:
            self.state[7] = self.val
            self.end = True
            self.winner = self.whose_turn()
            reward += 1
        return reward

    def play(self, row, col):
        if self.end:
            return False, -2  # loose
        if not self.board[row][col] == 0:
            return False, -2  # penalize on typing on filled slot

        self.board[row][col] = self.val
        self.number_of_empty -= 1

        reward = self.get_reward(row, col)

        # switch player
        self.val *= -1
        return True, reward
