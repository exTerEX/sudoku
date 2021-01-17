#!/usr/bin/env python3

class Board:
    def __init__(self, board_file):
        self.board = self._create_board(board_file)

    def _create_board(self, board_file):
        board = []

        for line in board_file:
            line = line.strip()

            if len(line) != 9:
                raise RuntimeError("Each line in the sudoku puzzle must be 9 chars long.")

            board.append([])

            for char in line:
                if not char.isdigit():
                    raise RuntimeError("Valid characters for a sudoku puzzle must be in 0-9")

                board[-1].append(int(char))

        if len(board) != 9:
            raise RuntimeError("Each sudoku puzzle must be 9 lines long")

        return board
