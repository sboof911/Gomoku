import numpy as np

MAX_SCORE = 200

def evaluate(board, board_array, player, x_value, y_value):
        absulute_win = [0, 1, 1, 1, 1, 0]
        directions = ["Horizontal", "Vertical", "Normal_Diag", "Reversed_Diag"]
        adjucents = board.get_Adjucents(x_value, y_value, 6)
        score = 0
        for direction in directions:
            count = 0
            curr_score = 2
            has_empty_side = False
            length = 0
            for key, (x, y) in enumerate(adjucents[direction]):
                if x is not None and y is not None:
                    if board_array[y][x] == (absulute_win[count]*player.stone_color):
                        count += 1
                        if count == len(absulute_win):
                            return MAX_SCORE
                    elif count > 0:
                        count = 0
                        if board_array[y][x] == (absulute_win[count]*player.stone_color):
                            count += 1

                    if board_array[y][x] == player.stone_color:
                        length += 1
                    else:
                        if board_array[y][x] == player.ZERO:
                            has_empty_side = True
                        else:
                            has_empty_side = False
                        if 0 <= key-(length+1) and not has_empty_side:
                            x0 = adjucents[direction][key-(length+1)][0]
                            y0 = adjucents[direction][key-(length+1)][1]
                            if x0 is not None and y0 is not None:
                                if board_array[y0][x0] == player.ZERO:
                                    has_empty_side = True
                        if length > curr_score and has_empty_side:
                            curr_score = length
                        length = 0
            score += curr_score

        return score*player.peer_captured

def heuristic_evaluation(board, board_array, player, winner, x, y, DRAW, depth):
    if winner == DRAW:
        return 0
    elif winner != None:
        return MAX_SCORE*player.stone_color*depth

    score = evaluate(board, board_array, player, x, y)
    return score*player.stone_color

