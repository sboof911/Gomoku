import numpy as np
from srcs.backend.game.player import player

class board:
    def __init__(self, board_size, connect_num) -> None:
        self._connect_num = connect_num
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

    def check_horizontal(self, board_array, i, j, stone_color):
        if np.all(board_array[i, j:j+self._connect_num] == stone_color):
            line_pos = self._get_line_pos(j+1, i+1, j+self._connect_num, i+1)
            return True, line_pos

        return False, None

    def check_vertical(self, board_array, i, j, stone_color):
        if np.all(board_array[j:j+self._connect_num, i] == stone_color):
            line_pos = self._get_line_pos(i+1, j+1, i+1, j+self._connect_num)
            return True, line_pos

        return False, None

    def check_diag(self, board_array, i, j, stone_color):
        if i < self._size - (self._connect_num - 1):
            if np.all(np.diagonal(board_array[i:i+self._connect_num, j:j+self._connect_num]) == stone_color):
                line_pos = self._get_line_pos(j+1, i+1, j+self._connect_num, i+self._connect_num)
                return True, line_pos

            if np.all(np.diagonal(np.fliplr(board_array[i:i+self._connect_num, j:j+self._connect_num])) == stone_color):
                line_pos = self._get_line_pos(j+self._connect_num, i+1, j+1, i+self._connect_num)
                return True, line_pos

        return False, None

    def terminal_state(self, stone_color, set_winner = True, board_array = None):
        board_array = self._board if board_array is None else board_array
        for i in range(self._size):
            for j in range(self._size - (self._connect_num - 1)):
                def check(line_pos):
                    if set_winner:
                        self._line_pos = line_pos
                        self._board_winner_color = stone_color
                        return True
                    return True, stone_color

                is_win, line_pos = self.check_horizontal(board_array, i, j, stone_color)
                if is_win:
                    return check(line_pos)
                is_win, line_pos = self.check_vertical(board_array, i, j, stone_color)
                if is_win:
                    return check(line_pos)
                is_win, line_pos = self.check_diag(board_array, i, j, stone_color)
                if is_win:
                    return check(line_pos)

        if not np.any(board_array == player.ZERO):
            if set_winner:
                self._board_winner_color = player.DRAW
                return True
            else:
                return True, player.DRAW
        return False if set_winner else (False, None)
