from time import time
from srcs.ai.Minimax import minimax, MAX_SCORE, get_best_available_actions

class AI_manager():
    BLACK = 1
    DRAW = MAX_SCORE**2
    WHITE = -1 * BLACK
    ZERO = 0 * BLACK

    def __init__(self, difficulty, debug_mode=False) -> None:
        self._difficulty = difficulty
        self._debug_mode = debug_mode
        self._ai_isThinking = False
        self._memo = {}

    def get_depth(self):
        if self._difficulty == 1:
            return 3
        elif self._difficulty == 2:
            return 7
        elif self._difficulty == 3:
            return 11
        raise Exception("Difficulty level not supported")

    def get_best_move(self, board, players, current_player_index):
        self._board = board
        self._depth = self.get_depth()
        self._players = players
        current_time = time()

        if len(board._used_actions) == 0:
            center = self._board._size//2
            return center, center

        if not self._ai_isThinking:
            self._ai_isThinking = True
            players_clone = [player.clone() for player in players]
            _, x, y = minimax(board, board._board.copy(), self._depth,
                              players_clone, current_player_index,
                              used_actions=board._used_actions.copy(),
                              memo = self._memo)
            if x is None or y is None:
                x, y = get_best_available_actions(board._board, board._used_actions, self.ZERO)[0]
            self._ai_isThinking = False
        else:
            raise Exception("AI is already thinking")

        if self._debug_mode:
            print("Can't print the time, debug mode is on")
        else:
            print(f"Time to get best move:{time()-current_time:.2f}s")
        return x, y
