from time import time
from srcs.backend.ai.heuristic_evaluation import heuristic_evaluation

class Minimax:
    BLACK = 1
    DRAW = 80 * BLACK
    WHITE = -1 * BLACK
    ZERO = 0 * BLACK

    def __init__(self, depth=6, debug_mode=False) -> None:
        if self.BLACK == 0 or not isinstance(self.BLACK, int):
            raise Exception("BLACK ID MUST BE AN INT DIFFERENT THEN 0")
        from srcs.backend.game.board import board as board_module

        self._depth = depth
        self._board : board_module = None
        self._debug_mode = debug_mode

    def get_best_available_actions(self, board_array, x0=-2, y0=-2):
        available_actions = set()
        if x0 == -2 and y0 == -2:
            if not self._board._used_actions:
                center = self._board._size//2
                used_actions = [(center, center)]
            else:
                used_actions = self._board._used_actions
        else:
            used_actions = [(x0, y0)]

        for x, y in used_actions:
            boarder_num = 2
            for y1 in range(y-boarder_num,y+boarder_num+1):
                for x1 in range(x-boarder_num,x+boarder_num+1):
                    if 0 <= x1 < self._board._size and 0 <= y1 < self._board._size:
                        if board_array[y1][x1] == self.ZERO:
                            available_actions.add((x1, y1))
        return available_actions

    def get_best_move(self, board, players, current_player_index):
        self._board = board
        board_array = self._board._board.copy()
        current_time = time()
        is_maximizing = True if players[current_player_index].stone_color == self.BLACK else False

        _, x, y = self.minimax(board_array, self._depth, is_maximizing, players, current_player_index)
        if self._debug_mode:
            print("Can't print the time, debug mode is on")
        else:
            print(f"Time to get best move:{time()-current_time:.2f}s")
        return x, y

    def minimax(self, board_array, depth, is_maximizing, players, current_player_index,
                x=-2, y=-2, alpha=float('-inf'), beta=float('inf')):
        # Terminal state

        if x >= 0 and y >= 0:
            opponent_player = players[(current_player_index + 1) % 2]
            game_over, winner = self._board.terminal_state(x, y, opponent_player, False, board_array)
            if game_over or depth == 0:
                return heuristic_evaluation(self._board, board_array, opponent_player, winner,
                                            x, y, self.DRAW, depth), None, None

        # Maximizing player
        return_value = None
        available_actions = self.get_best_available_actions(board_array, x, y)

        if is_maximizing:
            max_eval = float('-inf')
            best_move = (None, None)
            for x, y in available_actions:
                players_copy = [player.clone() for player in players]
                played, board_array = self._board.place_stone(x, y, players_copy, current_player_index, board_array)
                if played:
                    eval, _, _ = self.minimax(board_array, depth - 1, False, players_copy, (current_player_index + 1) % 2, x, y, alpha, beta)
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
                    eval, _, _ = self.minimax(board_array, depth - 1, True, players_copy, (current_player_index + 1) % 2, x, y, alpha, beta)
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
