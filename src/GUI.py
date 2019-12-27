# GUI.py

import sys
import pygame

pygame.font.init()


class Deck(object):
    def __init__(self, deck, w, h, windowObject) -> object:
        self._rows, self._cols = len(deck), len(deck[0])
        self._deck = deck

        self._cube = []
        for i in range(self._rows):
            self._cube.append([])
            for j in range(self._cols):
                self._cube[i].append(Cube(self._deck[i][j], i, j, w, h))

        self._w, self._h = w, h
        self._model = None
        self._update_model()
        self._selected = None
        self._wObj = windowObject

    def _update_model(self):
        rows, cols = self._rows, self._cols

        self._model = []
        for i in range(rows):
            self._model.append([])
            for j in range(cols):
                self._model[i].append(self._cube[i][j].value)

    def place(self, value) -> bool:
        row, col = self._selected
        cube = self._cube

        if cube[row][col].value == 0:
            cube[row][col].set(value)
            self._update_model()

            if valid(self._model, value, (row, col)) and self._solve():
                return True
            else:
                cube[row][col].set(0)
                cube[row][col].set_temp(0)
                self._update_model()
                return False

    def sketch(self, value):
        row, col = self._selected

        self._cube[row][col].set_temp(value)

    def draw(self):
        wObj = self._wObj
        w, h = self._w, self._h
        rows, cols = self._rows, self._cols
        cube = self._cube

        gap = w / 9

        for i in range(rows + 1):
            if i % 3 == 0 and i != 0:
                line = 3
            else:
                line = 1

            pygame.draw.line(wObj, (0, 0, 0), (0, i * gap), (w, i * gap), line)

            pygame.draw.line(wObj, (0, 0, 0), (i * gap, 0), (i * gap, h), line)

        for row in range(rows):
            for col in range(cols):
                cube[row][col].draw(wObj)

    def select(self, row, col):
        rows, cols = self._rows, self._cols
        cube = self._cube

        for row in range(rows):
            for col in range(cols):
                cube[row][col].selected = False

        cube[row][col].selected = True
        self._selected = (row, col)

    def clear(self):
        row, col = self._selected

        if self._cube[row][col].value == 0:
            self._cube[row][col].set_temp(0)

    def click(self, pos) -> list:
        w, h = self._w, self._h

        if pos[0] < w and pos[1] < h:
            gap = w / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y), int(x))
        else:
            return None

    def is_finished(self) -> bool:
        rows, cols = self._rows, self._cols
        cube = self._cube

        for row in range(rows):
            for col in range(cols):
                if cube[row][col].value == 0:
                    return False
        return True

    def _solve(self) -> bool:
        model = self._model
        cube = self._cube
        wObj = self._wObj

        find = find_empty(model)

        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if valid(model, i, (row, col)):
                model[row][col] = i
                cube[row][col].set(i)
                cube[row][col]._draw_change(wObj, True)
                self._update_model()
                pygame.display.update()
                pygame.time.delay(100)

                if self._solve():
                    return True

                model[row][col] = 0
                cube[row][col].set(0)
                self._update_model()
                cube[row][col]._draw_change(self._wObj, False)
                pygame.display.update()
                pygame.time.delay(100)

        return False


class Cube(object):
    rows = 9
    cols = 9

    def __init__(self, value, row, col, w, h) -> object:
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self._w = w
        self._h = h
        self._selected = False

    def draw(self, _wObj):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self._w / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128, 128, 128))
            _wObj.blit(text, (x + 5, y + 5))
        elif not self.value == 0:
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            _wObj.blit(
                text,
                (
                    x + (gap / 2 - text.get_width() / 2),
                    y + (gap / 2 - text.get_height() / 2),
                ),
            )

        if self._selected:
            pygame.draw.rect(_wObj, (255, 0, 0), (x, y, gap, gap), 3)

    def _draw_change(self, _wObj, g=True):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self._w / 9
        x = self.col * gap
        y = self.row * gap

        pygame.draw.rect(_wObj, (255, 255, 255), (x, y, gap, gap), 0)
        text = fnt.render("", 1, (0, 0, 0))
        if self.value != 0:
            text = fnt.render(str(self.value), 1, (0, 0, 0))

        _wObj.blit(
            text,
            (
                x + (gap / 2 - text.get_width() / 2),
                y + (gap / 2 - text.get_height() / 2),
            ),
        )

        if g:
            pygame.draw.rect(_wObj, (0, 255, 0), (x, y, gap, gap), 1)
        else:
            pygame.draw.rect(_wObj, (0, 0, 0), (x, y, gap, gap), 1)

    def set(self, value):
        self.value = value

    def set_temp(self, value):
        self.temp = value


def valid(deck, n, pos):
    for x in range(len(deck)):
        if deck[x][pos[1]] == n and pos[0] != x:
            return False

    for y in range(len(deck[0])):
        if deck[pos[0]][y] == n and pos[1] != y:
            return False

    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for x in range(box_y * 3, box_y * 3 + 3):
        for y in range(box_x * 3, box_x * 3 + 3):
            if deck[x][y] == n and (x, y) != pos:
                return False

    return True


def find_empty(deck) -> list:
    for x in range(len(deck)):
        for y in range(len(deck[0])):
            if deck[x][y] == 0:
                return (x, y)
    return None


def redraw_window(winObj, deck, strikes):
    winObj.fill((255, 255, 255))
    fnt = pygame.font.SysFont("comicsans", 40)
    text = fnt.render("X " * strikes, 1, (255, 0, 0))
    winObj.blit(text, (20, 540))
    deck.draw()


if __name__ == "__main__":
    deck_matrix = []

    file = str(sys.argv[1])
    infile = open("deck/" + file, "r")

    for index, line in enumerate(infile.readlines()):
        line = line.split(",")
        deck_matrix.append([])
        for element in line:
            deck_matrix[index].append(int(element))

    print(deck_matrix)

    win = pygame.display.set_mode((540, 540))
    pygame.display.set_caption("Sudoku")
    deck = Deck(deck_matrix, 540, 540, win)

    key = None
    run = True
    strikes = 0

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    deck._solve()

        redraw_window(win, deck, strikes)
        pygame.display.update()
    pygame.quit()
