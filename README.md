# Sudoku

A simple project creating a sudoku solver and visualizer using the [Backtracking](https://en.wikipedia.org/wiki/Backtracking) algorithm with a few samples of initial sudoku deck's.

## Requirements

- [python](https://www.python.org/)
- [pip](https://pip.pypa.io/en/stable/)

## Setup

Install python packages,

```sh
~$ git clone https://github.com/exTerEX/sudoku.git
~$ cd sudoku/
~$ pip install -r tests/requirements.txt
```

## Start program

In `src/` find [GUI.py](src/GUI.py) and launch it with python. This can be done from terminal using,

```sh
~$ cd src/
~$ python GUI.py <filename>
```

The `Filename` is in [src/deck/](src/deck/) and contain the initial state of a sudoku puzzle.

To run the autosolver, press the `spacebar` on your keyboard.

## License

This project is unlicenced. See [LICENSE](LICENSE) for futher details.
