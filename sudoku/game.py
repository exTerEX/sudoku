#!/usr/bin/env python3

# pyright: reportMissingImports=false
from board import Board


class Game:
    def __init__(self, board_file):
        self.board_file = board_file
        self.start_puzzle = Board(board_file).puzzle

    def start(self):
        self.game_over = False
        self.puzzle = []

        for index in range(9):
            self.puzzle.append([])

            for jndex in range(9):
                self.puzzle[index].append(self.start_puzzle[index][jndex])

    def check_win(self):
        for row in range(9):
            if not self._check_row(row):
                return False
        for column in range(9):
            if not self._check_column(column):
                return False
        for row in range(3):
            for column in range(3):
                if not self._check_square(row, column):
                    return False
        self.game_over = True
        return True

    def _check_block(self, block):
        return set(block) == set(range(1, 10))

    def _check_row(self, row):
        return self._check_block(self.puzzle[row])

    def _check_column(self, column):
        return self._check_block(
            [self.puzzle[row][column] for row in range(9)]
        )

    def _check_square(self, row, column):
        return self._check_block(
            [
                self.puzzle[r][c]
                for r in range(row * 3, (row + 1) * 3)
                for c in range(column * 3, (column + 1) * 3)
            ]
        )
