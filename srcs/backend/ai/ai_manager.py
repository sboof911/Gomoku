import numpy as np
from time import time
from srcs.backend.ai.heuristic_evaluation import heuristic_evaluation

class Minimax:
    BLACK = 1
    DRAW = 80 * BLACK
    WHITE = -1 * BLACK
    ZERO = 0 * BLACK

    def __init__(self, depth=11, debug_mode=False) -> None:
        if self.BLACK == 0 or not isinstance(self.BLACK, int):
            raise Exception("BLACK ID MUST BE AN INT DIFFERENT THEN 0")
        from srcs.backend.game.board import board as board_module

        self._depth = depth
        self._board : board_module = None
        self._debug_mode = debug_mode

    def get_best_available_actions(self, board_array, used_actions):
        available_actions = set()
        if not used_actions:
            center = self._board._size//2
            directions = ["Horizontal", "Vertical", "Normal_Diag", "Reversed_Diag"]
            adjucents = self._board.get_Adjucents(center, center, 5)
            for direction in directions:
                for x, y in adjucents[direction]:
                    if x is not None and y is not None:
                        available_actions.add((x, y))
        else:
            for x, y in used_actions:
                if board_array[y][x] == self.ZERO:
                    available_actions.add((x, y))

        return available_actions

    def get_best_move(self, board, players, current_player_index):
        self._board = board
        board_array = self._board._board.copy()
        current_time = time()
        ismaximizing = True if players[current_player_index].stone_color == self.BLACK else False

        _, x, y = self.minimax(board_array, self._depth, ismaximizing, players, current_player_index, self._board._used_actions)
        if self._debug_mode:
            print("Can't print the time, debug mode is on")
        else:
            print(f"Time to get best move:{time()-current_time:.2f}s")
        return x, y

    def minimax(self, board_array, depth, is_maximizing, players, current_player_index,
                used_actions, x=-2, y=-2, alpha=float('-inf'), beta=float('inf')):
        # Terminal state
        if x >= 0 and y >= 0:
            opponent_player = players[(current_player_index + 1) % 2]
            game_over, winner = self._board.terminal_state(x, y, opponent_player, False, board_array)
            if game_over or depth == 0:
                return heuristic_evaluation(self._board, board_array, opponent_player, winner,
                                            x, y, DRAW=self.DRAW), None, None

        # Maximizing player
        return_value = None
        available_actions = self.get_best_available_actions(board_array, used_actions)
        if is_maximizing:
            max_eval = float('-inf')
            best_move = (None, None)
            for x, y in available_actions:
                players_copy = [player.clone() for player in players]
                played, board_array = self._board.place_stone(x, y, players_copy, current_player_index, board_array)
                if played:
                    used_actions.add((x, y))
                    eval, _, _ = self.minimax(board_array, depth - 1, False, players_copy, (current_player_index + 1) % 2, used_actions, x, y, alpha, beta)
                    used_actions.remove((x, y))
                    board_array[y][x] = players[0].ZERO
                    if eval > max_eval:
                        max_eval = eval
                        best_move = (x, y)
                    # Alpha-beta pruning
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break

            return_value = max_eval, best_move[0], best_move[1]

        # Minimizing player
        else:
            min_eval = float('inf')
            best_move = (None, None)
            for x, y in available_actions:
                players_copy = [player.clone() for player in players]
                played, board_array = self._board.place_stone(x, y, players_copy, current_player_index, board_array)
                if played:
                    available_actions_copy = available_actions.copy()
                    available_actions_copy.remove((x, y))
                    eval, _, _ = self.minimax(board_array, depth - 1, True, players, (current_player_index + 1) % 2, available_actions_copy, x, y, alpha, beta)
                    board_array[y][x] = players[0].ZERO
                    if eval < min_eval:
                        min_eval = eval
                        best_move = (x, y)
                    # Alpha-beta pruning
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break

            return_value = min_eval, best_move[0], best_move[1]

        return return_value
