from srcs.backend.ai.heuristic_evaluation import heuristic_evaluation, MAX_SCORE

def get_best_available_actions(board, ZERO, board_array, x1=-2, y1=-2, connect_num=2):
    available_actions = []
    directions = ["Horizontal", "Vertical", "Normal_Diag", "Reversed_Diag"]
    for x in range(board._size):
        for y in range(board._size):
            if board_array[y][x] == ZERO:
                adjucents = board.get_Adjucents(x, y, connect_num)
                found = False
                adj_to_last_play = False
                for direction in directions:
                    for x0, y0 in adjucents[direction]:
                        if x0 is not None and y0 is not None:
                            if board_array[y0][x0] != ZERO:
                                if x0==x1 and y0==y1:
                                    adj_to_last_play = True
                                found = True
                                break
                    if found:
                        if (x, y) not in available_actions:
                            if adj_to_last_play:
                                available_actions.insert(0, (x, y))
                            available_actions.append((x, y))
                        break

    return available_actions

def negamax(board, board_array, depth, players, current_player_index,
            x_value=-2, y_value=-2, alpha=float('-inf'), beta=float('inf'),
            queue_list=None, available_actions=None, scores=0):

    if x_value >= 0 and y_value >= 0:
        opponent_player = players[(current_player_index + 1) % 2]
        score = heuristic_evaluation(board_array, opponent_player, x_value, y_value, board._connect_num)
        scores += score*opponent_player.stone_color
        if score >= MAX_SCORE:
            return score*(depth+1), None, None
        elif depth == 0:
            return scores, None, None

    if not available_actions:
        available_actions = get_best_available_actions(board, players[0].ZERO, board_array, x_value, y_value)

    max_eval = float('-inf')
    best_move = (-1, -1)

    for x, y in available_actions:
        board_array_copy = board_array.copy()
        players_copy = [player.clone() for player in players]
        played, board_array_copy = board.place_stone(x, y, players_copy, current_player_index, board_array_copy)
        if played and board_array_copy[y][x] != players[0].ZERO:
            eval = negamax(board, board_array_copy, depth-1, players_copy, (current_player_index + 1) % 2, x, y, -beta, -alpha)[0]

            if eval > max_eval:
                max_eval = eval
                best_move = (x, y)

            alpha = max(alpha, eval)
            if alpha >= beta:
                break

    if queue_list:
        queue_list.put((max_eval, best_move[0], best_move[1]))

    return -max_eval, best_move[0], best_move[1]
