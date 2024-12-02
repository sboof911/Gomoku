from srcs.backend.ai.heuristic_evaluation import heuristic_evaluation, check_index, MAX_SCORE

def get_best_available_actions(board_array, used_actions, ZERO):
    available_actions = []
    directions = [(1, 1), (0, 1), (1, 0), (1, -1),
                  (0, -1), (-1, -1), (-1, 0), (-1, 1)]
    for x, y in used_actions:
        for dx, dy in directions:
            x0 = x + dx
            y0 = y + dy
            if check_index(board_array.shape[0], x0, y0):
                if board_array[y0][x0] == ZERO:
                    if (x0, y0) not in available_actions:
                        available_actions.append((x0, y0))

    center = board_array.shape[0] // 2
    available_actions.sort(key=lambda pos: abs(pos[0] - center) + abs(pos[1] - center))

    return available_actions

def undo_move(board_array, x, y, players, captured_stones_pos, used_actions, prev_captures):
    for x0, y0 in captured_stones_pos[0]:
        board_array[y0][x0] = players[0].BLACK
        used_actions.add((x0, y0))
    for x0, y0 in captured_stones_pos[1]:
        board_array[y0][x0] = players[0].WHITE
        used_actions.add((x0, y0))

    board_array[y][x] = players[0].ZERO
    used_actions.remove((x, y))
    players[0].peer_captured, players[1].peer_captured = prev_captures

def simulate_move(board, board_array, x, y, players, ai_player_index, maximizing_player, used_actions):
    opponent_player_index = (ai_player_index + 1) % 2
    current_player_index = ai_player_index if maximizing_player else opponent_player_index

    prev_captures = (players[0].peer_captured, players[1].peer_captured)

    played, board_array, captured_stones_pos = board.place_stone(
        x, y, players, current_player_index, board_array)

    if played:
        used_actions.add((x, y))
        for x0, y0 in captured_stones_pos[0]:
            used_actions.remove((x0, y0))
        for x0, y0 in captured_stones_pos[1]:
            used_actions.remove((x0, y0))

    return played, captured_stones_pos, prev_captures

def minimax(board, board_array, depth, players, ai_player_index,
            maximizing_player=True, alpha=float('-inf'),
            beta=float('inf'), used_actions={}):
    score = heuristic_evaluation(board_array, used_actions, players, ai_player_index, board._connect_num)

    if abs(score) >= MAX_SCORE or depth == 0:
        if score == players[0].DRAW:
            return 0, None, None
        return score, None, None

    available_actions = get_best_available_actions(board_array, used_actions, players[0].ZERO)
    max_eval = float('-inf')
    min_eval = float('inf')
    best_move = (available_actions[0][0], available_actions[0][1])

    for x, y in available_actions:
        played, captured_stones_pos, prev_captures = simulate_move(
            board, board_array, x, y, players, ai_player_index, maximizing_player, used_actions)

        if played:
            eval, _, _ = minimax(
                board, board_array, depth - 1, players,
                ai_player_index, not maximizing_player,
                alpha, beta, used_actions)

            undo_move(board_array, x, y, players, captured_stones_pos, used_actions, prev_captures)

            if maximizing_player:
                if eval > max_eval:
                    max_eval = eval
                    best_move = (x, y)
                alpha = max(alpha, eval)
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
