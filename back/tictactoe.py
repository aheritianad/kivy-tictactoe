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

    def check(self, row, col):
        horizontal = abs(self.board[row][0] +
                         self.board[row][1] + self.board[row][2]) == 3
        vertical = abs(self.board[0][col] + self.board[1]
                       [col] + self.board[2][col]) == 3
        diagonal = abs(self.board[0][0] + self.board[1]
                       [1] + self.board[2][2]) == 3
        antidiagonal = abs(self.board[0][2] +
                           self.board[1][1] + self.board[2][0]) == 3
        if self.number_of_empty == 0:
            self.end = True
            self.winner = None
        if horizontal:
            self.state[row] = self.val
            self.end = True
            self.winner = self.whose_turn()
        if vertical:
            self.state[3+col] = self.val
            self.end = True
            self.winner = self.whose_turn()
        if diagonal:
            self.state[6] = self.val
            self.end = True
            self.winner = self.whose_turn()
        if antidiagonal:
            self.state[7] = self.val
            self.end = True
            self.winner = self.whose_turn()

    def play(self, row, col):
        if self.end:
            return False
        if not self.board[row][col] == 0:
            return False

        self.board[row][col] = self.val
        self.number_of_empty -= 1

        self.check(row, col)

        # switch player
        self.val *= -1
        return True
