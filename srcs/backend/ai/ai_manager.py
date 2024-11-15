from time import time
from srcs.backend.ai.heuristic_evaluation import heuristic_evaluation, MAX_SCORE

class Minimax:
    BLACK = 1
    DRAW = 80 * BLACK
    WHITE = -1 * BLACK
    ZERO = 0 * BLACK

    def __init__(self, depth=3, debug_mode=False) -> None:
        if self.BLACK == 0 or not isinstance(self.BLACK, int):
            raise Exception("BLACK ID MUST BE AN INT DIFFERENT THEN 0")
        from srcs.backend.game.board import board as board_module

        self._depth = depth
        self._board : board_module = None
        self._debug_mode = debug_mode
        self._players = None

    # def get_best_available_actions(self, board_array, x0=-2, y0=-2, connect_num=2):
    #     available_actions = set()
    #     if x0 == -2 and y0 == -2:
    #         if not self._board._used_actions:
    #             center = self._board._size//2
    #             used_actions = [(center, center)]
    #         else:
    #             used_actions = self._board._used_actions
    #     else:
    #         used_actions = [(x0, y0)]

    #     for x, y in used_actions:
    #         for y1 in range(y-connect_num,y+connect_num+1):
    #             for x1 in range(x-connect_num,x+connect_num+1):
    #                 if 0 <= x1 < self._board._size and 0 <= y1 < self._board._size:
    #                     if board_array[y1][x1] == self.ZERO:
    #                         available_actions.add((x1, y1))

    #     return available_actions

    def get_best_available_actions(self, board_array, x0=-2, y0=-2, connect_num=2):
        available_actions = set()
        for x in range(self._board._size):
            for y in range(self._board._size):
                if board_array[y][x] == self.ZERO:
                    available_actions.add((x, y))

        return available_actions

    def get_best_move(self, board, players, current_player_index):
        self._board = board
        board_array = self._board._board
        self._players = players
        current_time = time()

        _, x, y = self.negamax(board_array, self._depth, current_player_index)
        if self._debug_mode:
            print("Can't print the time, debug mode is on")
        else:
            print(f"Time to get best move:{time()-current_time:.2f}s")
        return x, y

    def negamax(self, board_array, depth, current_player_index,
                x_value=-2, y_value=-2, alpha=float('-inf'), beta=float('inf')):
        # Terminal state
        if x_value >= 0 and y_value >= 0:
            opponent_player = self._players[(current_player_index + 1) % 2]
            game_over, winner = self._board.terminal_state(x_value, y_value, opponent_player, False, board_array)
            if game_over or depth == 0:
                score = heuristic_evaluation(self._board, board_array, opponent_player, winner,
                                            x_value, y_value, self.DRAW, depth)*opponent_player.stone_color
                return score, None, None

        available_actions = self.get_best_available_actions(board_array, x_value, y_value)
        max_eval = float('-inf')
        best_move = (0, 0)

        for x, y in available_actions:
            board_array_copy = board_array.copy()
            player1_capture = self._players[0].peer_captured
            player2_capture = self._players[1].peer_captured
            played, board_array_copy, captured_stones_pos = self._board.place_stone(x, y, self._players, current_player_index, board_array_copy)
            if played and board_array_copy[y][x] != self._players[0].ZERO:
                eval = self.negamax(board_array_copy, depth-1, (current_player_index + 1) % 2, x, y, -beta, -alpha)[0]
                self._players[0].peer_captured = player1_capture
                self._players[1].peer_captured = player2_capture
                if eval > max_eval:
                    max_eval = eval
                    best_move = (x, y)
                # Alpha-beta pruning
                alpha = max(alpha, eval)
                if alpha >= beta:
                    break

        return -max_eval, best_move[0], best_move[1]
