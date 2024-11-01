import numpy as np
from srcs.backend.ai.heuristic_evaluation import heuristic_evaluation

class Minimax:
    BLACK = 1
    DRAW = 80 * BLACK
    WHITE = -1 * BLACK
    ZERO = 0 * BLACK

    def __init__(self, board, rules, depth=4) -> None:
        if self.BLACK == 0 or not isinstance(self.BLACK, int):
            raise Exception("BLACK ID MUST BE AN INT DIFFERENT THEN 0")
        from srcs.backend.game.board import board as board_module
        from srcs.backend.game.rules_manager import rules as rules_module
        self._depth = depth
        self._board : board_module = board
        self._rules : rules_module = rules

    def get_best_move(self, stone_color):
        opponent_color = self.WHITE if stone_color == self.BLACK else self.BLACK
        board_array = self._board._board.copy()
        used_actions = self._board._used_actions.copy()
        if np.all(board_array == self.ZERO):
            center = self._board._size//2 + 1
            return center, center

        _, x, y = self.minimax(board_array, opponent_color, used_actions)
        return x+1, y+1

    def get_best_available_actions(self, used_actions, board_array):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        available_actions = set()
        for x, y in used_actions:
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < board_array.shape[1] and 0 <= ny < board_array.shape[0]:
                    if board_array[ny][nx] == self.ZERO:
                        available_actions.add((nx, ny))

        return available_actions

    def minimax(self, board_array : np.ndarray, opponent_color, used_actions,
                x=-1, y=-1, depth=0, alpha=-10000, beta=10000):
        stone_color = self.WHITE if opponent_color == self.BLACK else self.BLACK

        game_over = False
        if x>=0 and y>=0:
            game_over, winner = self._board.terminal_state(x, y, opponent_color, False, board_array)
            if depth == self._depth or game_over:
                return heuristic_evaluation(self._board, board_array, opponent_color, winner,
                                            x, y, DRAW=self.DRAW)

        best_score = 10000 * opponent_color
        best_move = (None, None)

        available_actions = self.get_best_available_actions(used_actions, board_array)

        for x, y in available_actions:
            if self._rules.is_legal(board_array, x, y):
                if board_array[y][x] != self.ZERO:
                    raise Exception("Something the AI went wrong, all the actions must be $ZERO")
                board_array[y][x] = stone_color
                used_actions.add((x, y))
                score, _, _ = self.minimax(board_array, stone_color, used_actions, x, y, depth+1, alpha, beta)
                used_actions.remove((x, y))
                board_array[y][x] = self.ZERO

                if stone_color == self.BLACK:
                    if score > best_score:
                        best_score = score
                        best_move = (x, y)
                    alpha = max(alpha, score)
                else:
                    if score < best_score:
                        best_score = score
                        best_move = (x, y)
                    beta = min(beta, score)

                if beta <= alpha:
                    break

        return best_score, best_move[0], best_move[1]
