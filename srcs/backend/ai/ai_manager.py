from time import time
from srcs.backend.ai.Minimax import negamax
from threading import Thread
from queue import Queue

class AI_manager():
    BLACK = 1
    DRAW = 80 * BLACK
    WHITE = -1 * BLACK
    ZERO = 0 * BLACK

    def __init__(self, depth=3, debug_mode=False) -> None:
        self._depth = depth
        self._debug_mode = debug_mode

    def get_best_move(self, board, players, current_player_index):
        self._board = board
        board_array = self._board._board
        self._players = players
        current_time = time()

        _, x, y = negamax(board, board_array, self._depth, players, current_player_index)
        if self._debug_mode:
            print("Can't print the time, debug mode is on")
        else:
            print(f"Time to get best move:{time()-current_time:.2f}s")
        return x, y
