import numpy as np

class Minimax:
    BLACK = 1
    DRAW = 80 * BLACK
    WHITE = -1 * BLACK
    ZERO = 0 * BLACK

    def __init__(self, board, rules, depth=6) -> None:
        if self.BLACK == 0 or not isinstance(self.BLACK, int):
            raise Exception("BLACK ID MUST BE AN INT DIFFERENT THEN 0")
        from srcs.backend.game.board import board as board_module
        from srcs.backend.game.rules_manager import rules as rules_module
        self._depth = depth
        self._board : board_module = board
        self._rules : rules_module = rules

    def get_best_move(self, stone_color):
        board_array = self._board._board.copy()
        actions_copy = self._board._actions.copy()
        opponent_color = self.WHITE if stone_color == self.BLACK else self.BLACK
        _, x, y = self.minimax(board_array, opponent_color, actions_copy)

        return y+1, x+1

    def minimax(self, board_array : np.ndarray, opponent_color, actions : list,
                x=None, y=None, depth=0):
        stone_color = self.WHITE if opponent_color == self.BLACK else self.BLACK

        game_over, winner = self._board.terminal_state(opponent_color, False, board_array)
        if depth == self._depth or game_over:
            return self.heuristic_evaluation(board_array, x, y, opponent_color, winner)

        best_score = 10000
        best_score = best_score * opponent_color
        copy_board = board_array.copy()
        best_move = (None, None)
        # scores = np.full((board_array.shape[0], board_array.shape[0]), self.ZERO, dtype=int)
        for x, y in actions:
            if self._rules.is_legal(copy_board, x, y):
                if copy_board[x][y] != self.ZERO:
                    raise Exception("Something the AI went wrong, all the actions must be $ZERO")
                copy_board[x][y] = stone_color
                actions_copy = actions.copy()
                actions_copy.remove((x, y))
                score, _, _ = self.minimax(copy_board, stone_color, actions_copy, x, y, depth+1)
                # score = (score * stone_color) / (depth+1)
                # scores[x][y] = score
                copy_board[x][y] = self.ZERO
                if (stone_color == self.BLACK and score > best_score) or (stone_color != self.BLACK and score < best_score):
                    best_score = score
                    best_move = (x, y)

        # print(f"depth = {depth}")
        # print("scores:")
        # print(scores)
        # print("-"*20)
        return best_score, best_move[0], best_move[1]

    def check_adjacents(self, board_array, x, y, stone_color, connect_num):
        score = 0
        for step in range(connect_num):
            if y - step > 0:
                score += 1 if self._board.check_horizontal(board_array, x, y-step, stone_color, connect_num)[0] else 0
            if x - step > 0:
                score += 1 if self._board.check_vertical(board_array, x-step, y, stone_color, connect_num)[0] else 0
            if  y - step > 0 and x - step > 0:
                score += 1 if self._board.check_diag(board_array, x-step, y-step, stone_color, connect_num)[0] else 0
        return score

    def heuristic_evaluation(self, board_array, x, y, stone_color, winner):
        if winner == self.DRAW:
            return (0, None, None)
        elif winner:
            return (100 * self._board._connect_num * stone_color, None, None)

        # return 1, None, None
        if winner == None:
            connect_num = self._board._connect_num - 1
            while connect_num > 1:
                score = self.check_adjacents(board_array, x, y, stone_color, connect_num)
                if score != 0:
                    return (score * connect_num * stone_color, None, None)
                connect_num = connect_num - 1
            return (stone_color, None, None)

