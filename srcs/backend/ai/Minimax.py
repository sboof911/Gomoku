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

def minimax(board, board_array, depth, players, ai_player_index,
            x_value=-2, y_value=-2, maximizing_player=True,
            alpha=float('-inf'), beta=float('inf'), available_actions=None):

    score = heuristic_evaluation(board_array, players, ai_player_index, board._connect_num)

    # if board._turns == 5 and x_value == 9 and y_value == 4:
        # print(f"[({x_value}, {y_value}) ---> {score} - {maximizing_player}]")
    if abs(score) >= MAX_SCORE or depth == 0:
        if score == players[0].DRAW:
            return 0, None, None
        return score, None, None

    if not available_actions:
        available_actions = get_best_available_actions(
            board, players[0].ZERO, board_array, x_value, y_value)

    opponent_player_index = (ai_player_index + 1) % 2
    max_eval = float('-inf')
    min_eval = float('inf')
    best_move = (-1, -1)

    for x, y in available_actions:
        board_array_copy = board_array.copy()
        players_copy = [player.clone() for player in players]
        if maximizing_player:
            played, board_array_copy = board.place_stone(
                x, y, players_copy, ai_player_index, board_array_copy)
        else:
            played, board_array_copy = board.place_stone(
                x, y, players_copy, opponent_player_index, board_array_copy)
        if played:
            eval, _, _ = minimax(
                board, board_array_copy, depth-1, players_copy,
                ai_player_index, x, y, not maximizing_player, alpha, beta)

        if maximizing_player:
            if eval > max_eval:
                max_eval = eval
                best_move = (x, y)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        else:
            if eval < min_eval:
                min_eval = eval
                best_move = (x, y)
            beta = min(beta, eval)
            if beta <= alpha:
                break

    if maximizing_player:
        return max_eval, best_move[0], best_move[1]
    return min_eval, best_move[0], best_move[1]