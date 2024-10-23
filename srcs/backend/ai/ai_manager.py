
class Minimax:
    BLACK = 1
    WHITE = -1
    DRAW = 2
    ZERO = 0
    def __init__(self, board, rules, depth=2) -> None:
        self._depth = depth
        self._board = board
        self._rules = rules

    def get_best_move(self, stone_color, board_array=None, depth=0):
        board_array = self._board._board.copy() if board_array is None else board_array.copy()
        best_move = None
        best_score = float('-inf')
        for x in range(self._board._size):
            for y in range(self._board._size):
                if board_array[x][y] == self.ZERO and self._rules.is_legal(board_array, x, y):
                    board_array[x][y] = stone_color
                    score = self.minimax(x, y, depth)
                    board_array[x][y] = self.ZERO

                    if score > best_score:
                        best_score = score
                        best_move = (y+1, x+1)

        return best_move

    def minimax(self, x, y, depth):
        if depth == self._depth:
            pass
        return 1
