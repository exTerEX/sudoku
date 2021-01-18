#!/usr/bin/env python3

from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM

# pyright: reportMissingImports=false
from game import Game

BOARDS = ["easy", "hard", "debug", "error"]
MARGIN = 20
SIDE = 50
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9
GRID_LEN = 9


class Interface(Frame):
    def __init__(self, parent, obj):
        self.game = obj
        Frame.__init__(self, parent)
        self.parent = parent

        self.row, self.col = -1, -1

        self.init()

    def init(self):
        self.parent.title("Sudoku")
        self.parent.wm_iconbitmap("sudoku/resources/logo/sudoku-icon.ico")
        self.pack(fill=BOTH)
        self.canvas = Canvas(self, width=WIDTH, height=HEIGHT)
        self.canvas.pack(fill=BOTH, side=TOP)
        clear_button = Button(self, text="Clear answers", command=self._clear_answers)
        clear_button.pack(fill=BOTH, side=BOTTOM)

        self._draw_grid()
        self._draw_puzzle()

        self.canvas.bind("<Button-1>", self._cell_clicked)
        self.canvas.bind("<Key>", self._key_pressed)

    def _draw_grid(self):
        for index in range(GRID_LEN + 1):
            color = "black" if index % 3 == 0 else "gray"

            # Vertical
            self.canvas.create_line(
                MARGIN + index * SIDE,
                MARGIN,
                MARGIN + index * SIDE,
                HEIGHT - MARGIN,
                fill=color)

            # Horizontal
            self.canvas.create_line(
                MARGIN,
                MARGIN + index * SIDE,
                WIDTH - MARGIN,
                MARGIN + index * SIDE,
                fill=color)

    def _draw_puzzle(self):
        self.canvas.delete("numbers")

        for index in range(GRID_LEN):
            for jndex in range(GRID_LEN):
                answer = self.game._useradd_puzzle[index][jndex]

                if answer != 0:
                    color = "black" if answer == self.game._initial_puzzle[index][jndex] else "sea green"

                    self.canvas.create_text(
                        MARGIN + jndex * SIDE + SIDE / 2,
                        MARGIN + index * SIDE + SIDE / 2,
                        text=answer,
                        tags="numbers",
                        fill=color)

    def _draw_cursor(self):
        self.canvas.delete("cursor")

        if self.row >= 0 and self.col >= 0:
            self.canvas.create_rectangle(
                MARGIN + self.col * SIDE + 1,
                MARGIN + self.row * SIDE + 1,
                MARGIN + (self.col + 1) * SIDE - 1,
                MARGIN + (self.row + 1) * SIDE - 1,
                outline="red",
                tags="cursor")

    def _draw_victory(self):
        self.canvas.create_oval(
            MARGIN + SIDE * 2,
            MARGIN + SIDE * 2,
            MARGIN + SIDE * 7,
            MARGIN + SIDE * 7,
            tags="victory",
            fill="dark orange",
            outline="orange")

        self.canvas.create_text(
            MARGIN + 4 * SIDE + SIDE / 2,
            MARGIN + 4 * SIDE + SIDE / 2,
            text="You win!",
            tags="victory",
            fill="white",
            font=("Arial", 32))

    def _cell_clicked(self, event):
        if self.game._game_over_status:
            return

        x_pos, y_pos = event.x, event.y
        if (MARGIN < x_pos < WIDTH - MARGIN and MARGIN < y_pos < HEIGHT - MARGIN):
            self.canvas.focus_set()

            row, col = int((y_pos - MARGIN) / SIDE), int((x_pos - MARGIN) / SIDE)

            if (row, col) == (self.row, self.col):
                self.row, self.col = -1, -1
            elif self.game._useradd_puzzle[row][col] == 0:
                self.row, self.col = row, col
        else:
            self.row, self.col = -1, -1

        self._draw_cursor()

    def _key_pressed(self, event):
        if self.game._game_over_status:
            return

        if self.row >= 0 and self.col >= 0 and event.char in "1234567890":
            self.game._useradd_puzzle[self.row][self.col] = int(event.char)
            self.col, self.row = -1, -1

            self._draw_puzzle()
            self._draw_cursor()

            if self.game.check_win():
                self._draw_victory()

    def _clear_answers(self):
        self.game.start()
        self.canvas.delete("victory")
        self._draw_puzzle()


if __name__ == "__main__":
    NAME = "easy"

    with open(f"sudoku/resources/deck/{NAME}.sudoku", "r") as file:
        game = Game(file)
        game.start()

        root = Tk()

        Interface(root, game)

        root.geometry(f"{WIDTH}x{HEIGHT + 40}")
        root.mainloop()
