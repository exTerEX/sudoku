#!/usr/bin/env python3

from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM

# pyright: reportMissingImports=false
from game import Game


class Interface(Frame):
    def __init__(self, parent, obj, margin=20, side=50):
        Frame.__init__(self, parent)

        self.game = obj
        self.parent = parent

        self.row, self.col = -1, -1

        self._margin = margin
        self._side = side
        self._height = margin * 2 + side * 9
        self._width = margin * 2 + side * 9

        self.init()

    def init(self):
        self.parent.title("Sudoku")
        self.parent.wm_iconbitmap("game/resources/logo/sudoku-icon.ico")
        self.pack(fill=BOTH)
        self.canvas = Canvas(self, width=self._width, height=self._height)
        self.canvas.pack(fill=BOTH, side=TOP)
        clear_button = Button(self, text="Clear answers", command=self._clear_answers)
        clear_button.pack(fill=BOTH, side=BOTTOM)

        self._draw_grid()
        self._draw_puzzle()

        self.canvas.bind("<Button-1>", self._cell_clicked)
        self.canvas.bind("<Key>", self._key_pressed)

    def _draw_grid(self):

        margin = self._margin
        side = self._side
        height = self._height
        width = self._width

        for index in range(9 + 1):
            color = "black" if index % 3 == 0 else "gray"

            # Vertical
            self.canvas.create_line(
                margin + index * side,
                margin,
                margin + index * side,
                height - margin,
                fill=color)

            # Horizontal
            self.canvas.create_line(
                margin,
                margin + index * side,
                width - margin,
                margin + index * side,
                fill=color)

    def _draw_puzzle(self):
        self.canvas.delete("numbers")

        margin = self._margin
        side = self._side

        for index in range(9):
            for jndex in range(9):
                answer = self.game._useradd_puzzle[index][jndex]

                if answer != 0:
                    color = "sea green"
                    if answer == self.game._initial_puzzle[index][jndex]:
                        color = "black"

                    self.canvas.create_text(
                        margin + jndex * side + side / 2,
                        margin + index * side + side / 2,
                        text=answer,
                        tags="numbers",
                        fill=color)

    def _draw_cursor(self):
        self.canvas.delete("cursor")

        margin = self._margin
        side = self._side

        if self.row >= 0 and self.col >= 0:
            self.canvas.create_rectangle(
                margin + self.col * side + 1,
                margin + self.row * side + 1,
                margin + (self.col + 1) * side - 1,
                margin + (self.row + 1) * side - 1,
                outline="red",
                tags="cursor")

    def _draw_victory(self):
        margin = self._margin
        side = self._side

        self.canvas.create_oval(
            margin + side * 2,
            margin + side * 2,
            margin + side * 7,
            margin + side * 7,
            tags="victory",
            fill="dark orange",
            outline="orange")

        self.canvas.create_text(
            margin + 4 * side + side / 2,
            margin + 4 * side + side / 2,
            text="You win!",
            tags="victory",
            fill="white",
            font=("Arial", 32))

    def _cell_clicked(self, event):
        if self.game._game_over_status:
            return

        margin = self._margin
        width = self._width
        height = self._height
        side = self._side

        x_pos, y_pos = event.x, event.y
        if (margin < x_pos < width - margin and margin < y_pos < height - margin):
            self.canvas.focus_set()

            row, col = int((y_pos - margin) / side), int((x_pos - margin) / side)

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

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width


if __name__ == "__main__":
    NAME = "easy"

    with open(f"game/resources/deck/{NAME}.sudoku", "r") as file:
        game = Game(file)
        game.start()

        root = Tk()

        ui = Interface(root, game)

        root.geometry(f"{ui.width}x{ui.height + 40}")
        root.mainloop()
