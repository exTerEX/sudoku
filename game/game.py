#!/usr/bin/env python3

# pyright: reportMissingImports=false
from board import Board

GRID_LEN = 9
BOX_LEN = 3


class Game:
    def __init__(self, fp: str):
        self._initial_puzzle = Board(fp).puzzle
        self._useradd_puzzle = []

        self._game_over_status = False

    def start(self):
        for index in range(GRID_LEN):
            self._useradd_puzzle.append([])

            for jndex in range(GRID_LEN):
                self._useradd_puzzle[index].append(self._initial_puzzle[index][jndex])

    def check_win(self):
        for row in range(GRID_LEN):
            if not self._check_row(row):
                return False

        for column in range(GRID_LEN):
            if not self._check_column(column):
                return False

        for row in range(BOX_LEN):
            for column in range(BOX_LEN):
                if not self._check_square(row, column):
                    return False

        self._game_over_status = True

        return True

    def _check_row(self, row):
        return set(self._useradd_puzzle[row]) == set(range(1, 10))

    def _check_column(self, column):
        return set([self._useradd_puzzle[row][column] for row in range(9)]) == set(range(1, 10))

    def _check_square(self, row, column):
        return set([self._useradd_puzzle[r][c]
                    for r in range(row * 3, (row + 1) * 3)
                    for c in range(column * 3, (column + 1) * 3)]) == set(range(1, 10))
