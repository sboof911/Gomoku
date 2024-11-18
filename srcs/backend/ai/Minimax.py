from srcs.backend.ai.heuristic_evaluation import heuristic_evaluation, MAX_SCORE

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

    #     directions = ["Horizontal", "Vertical", "Normal_Diag", "Reversed_Diag"]
    #     for x, y in used_actions:
    #         adjucents = self._board.get_Adjucents(x, y, connect_num)
    #         for key in range(len(adjucents[directions[0]])):
    #             for direction in directions:
    #                 x1 = adjucents[direction][key][0]
    #                 y1 = adjucents[direction][key][1]
    #                 if x1 is not None and y1 is not None:
    #                     if board_array[y1][x1] == self.ZERO:
    #                         available_actions.add((x1, y1))

    #     return available_actions
    
    # def get_best_available_actions(self, board_array, x0=-2, y0=-2, connect_num=2):
    #     available_actions = set()
    #     directions = ["Horizontal", "Vertical", "Normal_Diag", "Reversed_Diag"]
    #     for x in range(self._board._size):
    #         for y in range(self._board._size):
    #             if board_array[y][x] != self.ZERO:
    #                 adjucents = self._board.get_Adjucents(x, y, connect_num)
    #                 for key in range(len(adjucents[directions[0]])):
    #                     for direction in directions:
    #                         x1 = adjucents[direction][key][0]
    #                         y1 = adjucents[direction][key][1]
    #                         if x1 is not None and y1 is not None:
    #                             if board_array[y1][x1] == self.ZERO:
    #                                 available_actions.add((x1, y1))

    #     if len(available_actions) == 0:
    #         available_actions.add((self._board._size//2, self._board._size//2))
    #     return available_actions

def get_best_available_actions(board, ZERO, board_array, x0=-2, y0=-2, connect_num=2):
    available_actions = set()
    for x in range(board._size):
        for y in range(board._size):
            if board_array[y][x] == ZERO:
                available_actions.add((x, y))

    return available_actions

def negamax(board, board_array, depth, players, current_player_index,
            x_value=-2, y_value=-2, alpha=float('-inf'), beta=float('inf'),
            queue_list=None, available_actions=None):
    # Terminal state
    if x_value >= 0 and y_value >= 0:
        opponent_player = players[(current_player_index + 1) % 2]
        game_over, winner = board.terminal_state(x_value, y_value, opponent_player, False, board_array)
        if game_over or depth == 0:
            score = heuristic_evaluation(board, board_array, opponent_player, winner,
                                        x_value, y_value, players[0].DRAW, depth)*opponent_player.stone_color
            return score, None, None

    if not available_actions:
        available_actions = get_best_available_actions(board, players[0].ZERO, board_array, x_value, y_value)

    max_eval = float('-inf')
    best_move = (0, 0)
    for x, y in available_actions:
        board_array_copy = board_array.copy()
        players_copy = [player.clone() for player in players]
        played, board_array_copy = board.place_stone(x, y, players_copy, current_player_index, board_array_copy)
        if played and board_array_copy[y][x] != players[0].ZERO:
            eval = negamax(board, board_array_copy, depth-1, players_copy, (current_player_index + 1) % 2, x, y, -beta, -alpha)[0]

            if eval > max_eval:
                max_eval = eval
                best_move = (x, y)
            # Alpha-beta pruning
            alpha = max(alpha, eval)
            if alpha >= beta:
                break
            
    if queue_list:
        queue_list.put((max_eval, best_move[0], best_move[1]))

    return -max_eval, best_move[0], best_move[1]
