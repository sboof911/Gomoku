class Minimax:
    def __init__(self, board, rules, stone_color) -> None:
        self._board = board
        self._rules = rules
        self._board_array = board._board.copy()
        self.AI_player = stone_color

    def get_best_move(self):
        best_move = None
        best_score = float('-inf')
        for x in range(self._board._size):
            for y in range(self._board._size):
                if self._board_array[x][y] == 0 and self._rules.is_legal(self._board_array, x, y):
                    self._board_array[x][y] = self.stone_color
                    score = self.minimax()
                    self._board_array[x][y] = 0

                    if score > best_score:
                        best_score = score
                        best_move = (y+1, x+1)

        return best_move

    def minimax(self):
        return 1

class ai_manager:
    def __init__(self, stone_color, depth=3) -> None:
        self.stone_color = stone_color
        self.depth = depth

    def choose_move(self, board, rules):
        Ai = Minimax(board, rules, self.stone_color)

        return Ai.get_best_move()
