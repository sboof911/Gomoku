import numpy as np
from srcs.backend.game.player import player
from srcs.backend.game.utils.Line_Checker import Horiz, Vertic, Diag, Reversed_Diag

class board:
    def __init__(self, board_size, connect_num) -> None:
        self._connect_num = connect_num
        self._size = board_size
        self._board = np.full((board_size, board_size), player.ZERO, dtype=int)
        self._board_winner_color = None
        self._line_pos = None
        self._used_actions = set()

    def check_horizontal(self, board_array, x, y, stone_color, connect_num):
        connect_num = self._connect_num if connect_num is None else connect_num
        for i in range(connect_num):
            index = y - i
            if 0 <= index < self._size:
                if board_array[index][x] != stone_color:
                    break
                line_pos = Horiz(board_array, x, index, stone_color, connect_num)
                if line_pos is not None:
                    return True, line_pos
            else:
                break

        return False, None

    def check_vertical(self, board_array, x, y, stone_color, connect_num):
        connect_num = self._connect_num if connect_num is None else connect_num
        for i in range(connect_num):
            index = x - i
            if 0 <= index < self._size:
                if board_array[y][index] != stone_color:
                    break
                line_pos = Vertic(board_array, index, y, stone_color, connect_num)
                if line_pos is not None:
                    return True, line_pos
            else:
                break

        return False, None

    def check_Normal_diag(self, board_array, x, y, stone_color, connect_num):
        connect_num = self._connect_num if connect_num is None else connect_num
        for i in range(connect_num):
            index_x = x - i
            index_y = y - i
            if 0 <= index_x < self._size and 0 <= index_y < self._size:
                if board_array[index_y][index_x] != stone_color:
                    break
                line_pos = Diag(board_array, index_x, index_y, stone_color, connect_num)
                if line_pos is not None:
                    return True, line_pos
            else:
                break

        return False, None

    def check_Reversed_diag(self, board_array, x, y, stone_color, connect_num):
        connect_num = self._connect_num if connect_num is None else connect_num
        for i in range(connect_num):
            index_x = x + i
            index_y = y - i
            if 0 <= index_x < self._size and 0 <= index_y < self._size:
                if board_array[index_y][index_x] != stone_color:
                    break
                line_pos = Reversed_Diag(board_array, index_x, index_y, stone_color, connect_num)
                if line_pos is not None:
                    return True, line_pos
            else:
                break

        return False, None

    def been_captured(self, x, y, player: player, board_array):
        other_point = (self._connect_num // 2) + (self._connect_num % 2)
        for i in [-other_point, other_point]:
            index = y + i

    def check_capture(self, x, y, player: player, board_array):
        other_point = (self._connect_num // 2) + (self._connect_num % 2)
        peer_captured = 0
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

        for dx, dy in directions:
            for i in [-other_point, other_point]:
                nx, ny = x + i * dx, y + i * dy
                if 0 <= nx < self._size and 0 <= ny < self._size:
                    if board_array[ny][nx] == player.stone_color:
                        min_x, max_x = sorted([x, nx])
                        min_y, max_y = sorted([y, ny])
                        if dx == 1 and dy == 0:  # horizontal
                            check_array = board_array[y, min_x + 1:max_x]
                        elif dx == 0 and dy == 1:  # vertical
                            check_array = board_array[min_y + 1:max_y, x]
                        elif dx == 1 and dy == 1:  # diagonal
                            check_array = np.diag(board_array[min_y + 1:max_y, min_x + 1:max_x])
                        elif dx == 1 and dy == -1:  # reversed diagonal
                            check_array = np.diag(np.fliplr(board_array[min_y + 1:max_y, min_x + 1:max_x]))

                        if len(check_array) == other_point - 1 and np.all(check_array == -player.stone_color):
                            peer_captured += 1
                            if dx == 1 and dy == 0:  # horizontal
                                board_array[y, min_x + 1:max_x] = player.ZERO
                            elif dx == 0 and dy == 1:  # vertical
                                board_array[min_y + 1:max_y, x] = player.ZERO
                            elif dx == 1 and dy == 1:  # diagonal
                                np.fill_diagonal(board_array[min_y + 1:max_y, min_x + 1:max_x], player.ZERO)
                            elif dx == 1 and dy == -1:  # reversed diagonal
                                sub_array = board_array[min_y + 1:max_y, min_x + 1:max_x]
                                flipped_sub_array = np.fliplr(sub_array)
                                np.fill_diagonal(flipped_sub_array, player.ZERO)
                                board_array[min_y + 1:max_y, min_x + 1:max_x] = np.fliplr(flipped_sub_array)

        return board_array, peer_captured

    def place_stone(self, x, y, player: player, board_array=None):
        board_array = self._board if board_array is None else board_array
        if 0 <= x < self._size and 0 <= y < self._size:
            if board_array[y][x] == player.ZERO:
                board_array[y][x] = player.stone_color
                board_array, peer_captured = self.check_capture(x, y, player, board_array.copy())
                player.peer_captured += peer_captured
                return True, board_array

        return False, board_array

    def check_line_win(self, x, y, stone_color, board_array, set_winner):
        def check(line_pos):
            if set_winner:
                self._line_pos = line_pos
                self._board_winner_color = stone_color
            return True, stone_color

        for check_method in [self.check_horizontal, self.check_vertical, self.check_Normal_diag, self.check_Reversed_diag]:
            is_win, line_pos = check_method(board_array, x, y, stone_color, self._connect_num)
            if is_win:
                return check(line_pos)
        return False, None

    def terminal_state(self, x, y, player : player, set_winner=True, board_array=None):
        if player.peer_captured >= 10:
            if set_winner:
                self._board_winner_color = player.stone_color
                return True
            return True, player.stone_color
        board_array = self._board if board_array is None else board_array
        line_win = self.check_line_win(x, y, player.stone_color, board_array, set_winner)
        if line_win[0]:
            if set_winner:
                return True
            return line_win

        if np.all(board_array != player.ZERO):
            if set_winner:
                self._board_winner_color = player.DRAW
                return True
            else:
                return True, player.DRAW

        return False if set_winner else (False, None)
