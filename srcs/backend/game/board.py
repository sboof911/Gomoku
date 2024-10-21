import numpy as np

class Game_Status:
    PLAYING = 0
    WINNER = 1

class board:
    def __init__(self) -> None:
        self._board = np.zeros((19, 19), dtype=int)


    def set_move(self, x, y, player_num):
        if x > 19 or x < 0 or y > 19 or y < 0:
            return False

        if self._board[y][x] == 0:
            self._board[y][x] = player_num
            return True

        return False
