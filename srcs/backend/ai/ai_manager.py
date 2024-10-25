
class Minimax:
    BLACK = 1
    WHITE = -1 * BLACK
    DRAW = 0
    ZERO = 2

    def __init__(self, board, rules, depth=1) -> None:
        self._depth = depth
        self._board = board
        self._rules = rules

    def get_best_move(self, stone_color, board_array=None, depth=0):
        board_array = self._board._board.copy() if board_array is None else board_array.copy()
        best_move = None
        best_score = (self._board._size**2 * 2)
        best_score = best_score * self.WHITE if stone_color == self.BLACK else best_score * self.BLACK
        for x in range(self._board._size):
            for y in range(self._board._size):
                if board_array[x][y] == self.ZERO and self._rules.is_legal(board_array, x, y):
                    board_array[x][y] = stone_color
                    score = self.minimax(board_array, stone_color, depth)
                    board_array[x][y] = self.ZERO

                    if (stone_color == self.BLACK and score > best_score) or (stone_color != self.BLACK and score < best_score):
                        best_score = score
                        best_move = (y + 1, x + 1)

        return best_move if depth == 0 else best_score

    def heuristic_evaluation(self, board_array, winner):
        if winner == None:
            return 0
        return winner

    def minimax(self, board_array, stone_color, depth):
        game_over, winner = self._board.terminal_state(stone_color, False, board_array)
        if depth == self._depth or game_over:
            return self.heuristic_evaluation(board_array, winner)
        next_stone = self.WHITE if stone_color == self.BLACK else self.BLACK
        return self.get_best_move(next_stone, board_array, depth+1)
