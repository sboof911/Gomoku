import numpy as np
from srcs.backend.game.player import player

class board:
    def __init__(self, board_size, connect_num) -> None:
        self._connect_num = connect_num
        self._size = board_size
        self._board = np.full((board_size, board_size), player.ZERO, dtype=int)
        self._board_winner_color = None
        self._line_pos = None
        self._used_actions = set()

    def unset_stone(self, x, y):
        self._board[y][x] = player.ZERO

    def place_stone(self, x, y, stone_color):
        if x > self._size or x < 0 or y > self._size or y < 0:
            return False

        if self._board[y][x] == player.ZERO:
            self._board[y][x] = stone_color
            self._used_actions.add((x, y))
            return True

        return False

    def _get_line_pos(self, x0, y0, x1, y1):
        return dict(
            x0=x0+1,
            y0=y0+1,
            x1=x1+1,
            y1=y1+1
        )

    def check_horizontal(self, board_array, x, y, stone_color, connect_num = None):
        connect_num = self._connect_num if connect_num is None else connect_num
        for i in range(connect_num):
            index = y - i
            if index >= 0:
                if board_array[index][x] != stone_color:
                    break
                checker = board_array[index:index+connect_num, x]
                if np.all(checker == stone_color) and checker.size == connect_num:
                    line_pos = self._get_line_pos(x, index, x, index+(connect_num-1))
                    return True, line_pos
            else:
                break

        return False, None

    def check_vertical(self, board_array, x, y, stone_color, connect_num = None):
        connect_num = self._connect_num if connect_num is None else connect_num
        for i in range(connect_num):
            index = x - i
            if index >= 0:
                if board_array[y][index] != stone_color:
                    break
                checker = board_array[y, index:index+connect_num]
                if np.all(checker == stone_color) and checker.size == connect_num:
                    line_pos = self._get_line_pos(index, y, index+(connect_num-1), y)
                    return True, line_pos
            else:
                break

        return False, None
    
    def check_Normal_diag(self, board_array, x, y, stone_color, connect_num):
        for i in range(connect_num):
            x_index = x - i
            y_index = y - i
            if x_index >= 0 and y_index >= 0:
                if board_array[y_index][x_index] != stone_color:
                    break
                checker = board_array[y_index:y_index+connect_num, x_index:x_index+connect_num]
                if np.all(np.diagonal(checker) == stone_color) and checker.shape == (connect_num, connect_num):
                    line_pos = self._get_line_pos(x_index, y_index, x_index+(connect_num-1), y_index+(connect_num-1))
                    return True, line_pos
            else:
                break

        return False, None
    
    def check_Reversed_diag(self, board_array, x, y, stone_color, connect_num):
        for i in range(connect_num):
            x_index = x + i
            y_index = y - i
            if x_index < self._size and y_index >= 0 and x_index-connect_num:
                if board_array[y_index][x_index] != stone_color:
                    break
                checker = board_array[y_index:y_index+connect_num, x_index-connect_num+1:x_index+1]
                if np.all(np.diagonal(np.fliplr(checker)) == stone_color) and checker.shape == (connect_num, connect_num):
                    line_pos = self._get_line_pos(x_index, y_index, x_index-(connect_num-1), y_index+(connect_num-1))
                    return True, line_pos
            else:
                break

        return False, None

    def check_diag(self, board_array, x, y, stone_color, connect_num = None):
        connect_num = self._connect_num if connect_num is None else connect_num
        finished, line_pos = self.check_Normal_diag(board_array, x, y, stone_color, connect_num)
        if not finished:
            finished, line_pos = self.check_Reversed_diag(board_array, x, y, stone_color, connect_num)
        return finished, line_pos

    def terminal_state(self, x, y, stone_color, set_winner = True, board_array = None):
        board_array = self._board if board_array is None else board_array
        def check(line_pos):
            if set_winner:
                self._line_pos = line_pos
                self._board_winner_color = stone_color
                return True
            return True, stone_color

        is_win, line_pos = self.check_horizontal(board_array, x, y, stone_color)
        if is_win:
            return check(line_pos)
        is_win, line_pos = self.check_vertical(board_array, x, y, stone_color)
        if is_win:
            return check(line_pos)
        is_win, line_pos = self.check_diag(board_array, x, y, stone_color)
        if is_win:
            return check(line_pos)

        if np.all(board_array != player.ZERO):
            if set_winner:
                self._board_winner_color = player.DRAW
                return True
            else:
                return True, player.DRAW
        return False if set_winner else (False, None)
