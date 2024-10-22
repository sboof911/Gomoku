import numpy as np

def _set_pos(x0, y0, x1, y1):
    return dict(
        x0=x0,
        y0=y0,
        x1=x1,
        y1=y1
    )

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

    def check_horizontal(self, i, j):
        if np.all(self._board[i, j:j+5] == 1):
            return 1, _set_pos(j+1, i+1, j+5, i+1)
        elif np.all(self._board[i, j:j+5] == 2):
            return 2, _set_pos(j+1, i+1, j+5, i+1)

        return 0, None

    def check_vertical(self, i, j):
        if np.all(self._board[j:j+5, i] == 1):
            return 1, _set_pos(i+1, j+1, i+1, j+5)
        elif np.all(self._board[j:j+5, i] == 2):
            return 2, _set_pos(i+1, j+1, i+1, j+5)

        return 0, None

    def check_diag(self, i, j):
        if i < 15:
            if np.all(np.diagonal(self._board[i:i+5, j:j+5]) == 1):
                return 1, _set_pos(j+1, i+1, j+5, i+5)
            elif np.all(np.diagonal(self._board[i:i+5, j:j+5]) == 2):
                return 2, _set_pos(j+1, i+1, j+5, i+5)

            if np.all(np.diagonal(np.fliplr(self._board[i:i+5, j:j+5])) == 1):
                return 1, _set_pos(j+5, i+1, j+1, i+5)
            elif np.all(np.diagonal(np.fliplr(self._board[i:i+5, j:j+5])) == 2):
                return 2, _set_pos(j+5, i+1, j+1, i+5)

        return 0, None

    def check_winner(self):
        for i in range(19):
            for j in range(15):
                winner, pos = self.check_horizontal(i, j)
                if winner > 0:
                    return winner, pos
                winner, pos = self.check_vertical(i, j)
                if winner > 0:
                    return winner, pos
                winner, pos = self.check_diag(i, j)
                if winner > 0:
                    return winner, pos

        # Check if self._board is full (no 0s)
        if not np.any(self._board == 0):
            return 0, None  # No winner, and board is full
        return -1, None
