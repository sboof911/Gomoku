
def heuristic_evaluation(board, board_array, stone_color, winner, x, y, DRAW):
    def evaluate(connect_num, player_color):
        score = 0
        while connect_num > board._connect_num//2:
            kwargs = dict(
                board_array=board_array,
                x=x,
                y=y,
                stone_color=player_color,
                connect_num=connect_num
            )
            score += 1 if board.check_horizontal(**kwargs)[0] else 0
            score += 1 if board.check_vertical(**kwargs)[0] else 0
            score += 1 if board.check_Normal_diag(**kwargs)[0] else 0
            score += 1 if board.check_Reversed_diag(**kwargs)[0] else 0

            connect_num -= 1
        return score

    if winner == DRAW:
        return (0, None, None)
    elif winner != None:
        return ((board._connect_num**2)*stone_color, None, None)

    connect_num = board._connect_num - 1
    evaluate_opportunities = evaluate(connect_num, stone_color)
    opponent_color = -stone_color
    evaluate_opportunities += evaluate(connect_num, opponent_color)

    return (stone_color, None, None)
