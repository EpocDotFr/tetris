# Tetris

The [Tetris](https://en.wikipedia.org/wiki/Tetris) game, implemented in Python.

> TODO Screenshot

## Features

> TODO

## Prerequisites

Python 3. May eventually works with Python 2 (not tested).

## Installation

Clone this repo, and then the usual `pip install -r requirements.txt`.

## Usage

```
python run.py
```

## Controls

  - <kbd>ESC</kbd> closes the game
  - <kbd>PAUSE</kbd> pauses the game
  - <kbd>F1</kbd> starts a new game
  - <kbd>←</kbd> and <kbd>→</kbd> moves the Tetrimino respectively to the left and to the right
  - <kbd>↑</kbd> rotates the Tetrimino
  - <kbd>↓</kbd> makes the Tetrimino to fall faster

## How it works

This game is built on top of [PyGame](http://www.pygame.org/hifi.html). I obviously can't explain how it
works here, so you'll have to jump yourself in the source code. Start with the entry point, `run.py`.

Beside the game itself, I use [PyInstaller](http://www.pyinstaller.org/) to generate the executables. It packs up all the
game and its assets in a single executable file so players just have to run it with nothing to install. This task is
performed by the `build_*` scripts to be run in the corresponding OS.

## Credits

  - Icon by [Everaldo Coelho](https://www.iconfinder.com/icons/3459/computer_game_tetris_icon) (freeware)
  - Font by [Typodermic Fonts Inc](http://www.dafont.com/coolvetica.font) (freeware)
  - Tetris™ and Tetriminos™ are trademarks of The Tetris Company. This project isn't supported nor endorsed by The Tetris Company

## End words

If you have questions or problems, you can [submit an issue](https://github.com/EpocDotFr/tetris/issues).

You can also submit pull requests. It's open-source man!
