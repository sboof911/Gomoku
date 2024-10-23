import numpy as np
from srcs.backend.game.player import player

class board:
    def __init__(self, board_size) -> None:
        self._size = board_size
        self._board = np.full((board_size, board_size), player.ZERO, dtype=int)
        self._board_winner_color = None
        self._line_pos = None

    def unset_stone(self, x, y):
        self._board[y][x] = player.ZERO

    def place_stone(self, x, y, stone_color):
        if x > self._size or x < 0 or y > self._size or y < 0:
            return False

        if self._board[y][x] == player.ZERO:
            self._board[y][x] = stone_color
            return True

        return False
    
    def _get_line_pos(self, x0, y0, x1, y1):
        return dict(
            x0=x0,
            y0=y0,
            x1=x1,
            y1=y1
        )

    def check_horizontal(self, i, j, stone_color):
        if np.all(self._board[i, j:j+5] == stone_color):
            line_pos = self._get_line_pos(j+1, i+1, j+5, i+1)
            return True, line_pos

        return False, None

    def check_vertical(self, i, j, stone_color):
        if np.all(self._board[j:j+5, i] == stone_color):
            line_pos = self._get_line_pos(i+1, j+1, i+1, j+5)
            return True, line_pos

        return False, None

        # return False

    def check_diag(self, i, j, stone_color):
        if i < 15:
            if np.all(np.diagonal(self._board[i:i+5, j:j+5]) == stone_color):
                line_pos = self._get_line_pos(j+1, i+1, j+5, i+5)
                return True, line_pos

            if np.all(np.diagonal(np.fliplr(self._board[i:i+5, j:j+5])) == stone_color):
                line_pos = self._get_line_pos(j+5, i+1, j+1, i+5)
                return True, line_pos

        return False, None

    def terminal_state(self, set_winner = True):
        for i in range(self._size):
            for j in range(self._size - 4):
                for stone_color in [player.BLACK, player.WHITE]:
                    def check(line_pos):
                        if set_winner:
                            self._line_pos = line_pos
                            self._board_winner_color = stone_color
                            return True
                        return True, stone_color

                    is_win, line_pos = self.check_horizontal(i, j, stone_color)
                    if is_win:
                        return check(line_pos)
                    is_win, line_pos = self.check_vertical(i, j, stone_color)
                    if is_win:
                        return check(line_pos)
                    is_win, line_pos = self.check_diag(i, j, stone_color)
                    if is_win:
                        return check(line_pos)

        if not np.any(self._board == player.ZERO):
            if set_winner:
                self._board_winner_color = player.DRAW
                return True
            else:
                return True, player.DRAW
        return False if set_winner else (False, None)
