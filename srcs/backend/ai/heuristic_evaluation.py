
def heuristic_evaluation(board, board_array, stone_color, winner, x, y, DRAW):
    if winner == DRAW:
        return (0, None, None)
    elif winner != None:
        return ((board._connect_num**2)*stone_color, None, None)

    connect_num = board._connect_num - 1
    while connect_num > board._connect_num//2:
        score = 1 if board.check_horizontal(board_array, x, y, stone_color, connect_num)[0] else 0
        score += 1 if board.check_vertical(board_array, x, y, stone_color, connect_num)[0] else 0
        score += 1 if board.check_Normal_diag(board_array, x, y, stone_color, connect_num)[0] else 0
        score += 1 if board.check_Reversed_diag(board_array, x, y, stone_color, connect_num)[0] else 0
        if score > 0:
            return (score*stone_color*connect_num, None, None)
        connect_num -= 1

    return (stone_color, None, None)