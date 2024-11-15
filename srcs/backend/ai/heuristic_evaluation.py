MAX_SCORE = 500

def evaluate(board, board_array, player, x_value, y_value):
        directions = ["Horizontal", "Vertical", "Normal_Diag", "Reversed_Diag"]
        adjucents = board.get_Adjucents(x_value, y_value)
        score = player.peer_captured ** 2
        pos = len(adjucents[directions[0]]) // 2 

        for direction in directions:
            continue_negtive, continue_positive = True, True
            last_positive, last_negative = (None, None), (None, None)
            length = 1
            for i in range(1, board._connect_num):
                if continue_positive:
                    if pos+i < len(adjucents[direction]):
                        x0, y0 = adjucents[direction][pos+i]
                        if (x0 != None) and (y0 != None) and (board_array[y0][x0] == player.stone_color):
                            length += 1
                        else:
                            last_positive = (x0, y0)
                            continue_positive = False
                if continue_negtive:
                    if pos-i >= 0:
                        x0, y0 = adjucents[direction][pos-i]
                        if (x0 != None) and (y0 != None) and (board_array[y0][x0] == player.stone_color):
                            length += 1
                        else:
                            last_negative = (x0, y0)
                            continue_negtive = False

            x1, y1 = last_positive
            x0, y0 = last_negative
            has_empty_left_side = (x1 is not None and y1 is not None and board_array[y1][x1] == player.ZERO)
            has_empty_right_side = (x0 is not None and y0 is not None and board_array[y0][x0] == player.ZERO)

            if has_empty_left_side or has_empty_right_side:
                if has_empty_left_side and has_empty_right_side:
                    if length == board._connect_num-1:
                        return MAX_SCORE
                    score += 1
                score += length*2
            else:
                score += 1

        return score

def heuristic_evaluation(board, board_array, player, winner, x, y, DRAW, depth):
    if winner == DRAW:
        return 0
    elif winner != None:
        return MAX_SCORE

    return evaluate(board, board_array, player, x, y)





###############################################################
MAX_SCORE = float('inf') - 100

def check_index(board, x, y):
    if x < 0 or y < 0:
        return False
    if x >= board.shape[1] or y >= board.shape[0]:
        return False
    return True

def nb_in_line(board, x, y, dx, dy, stone_color):
    ttl = 1
    free_extrems = 0
    blank = 0

    nx, ny = x + dx, y + dy
    while check_index(board, nx, ny) and board[ny][nx] == stone_color:
        nx += dx
        ny += dy
        ttl += 1
    if check_index(board, nx, ny) and board[ny][nx] != -stone_color:
        free_extrems += 1
        while check_index(board, nx, ny) and board[ny][nx] == 0 and blank + ttl < 6:
            nx += dx
            ny += dy
            blank += 1

    nx, ny = x - dx, y - dy
    while check_index(board, nx, ny) and board[ny][nx] == stone_color:
        nx -= dx
        ny -= dy
        ttl += 1
    if check_index(board, nx, ny) and board[ny][nx] != -stone_color:
        free_extrems += 1
        while check_index(board, nx, ny) and board[ny][nx] == 0 and blank + ttl < 6:
            nx -= dx
            ny -= dy
            blank += 1

    if blank + ttl < 5:
        return 0
    elif ttl >= 5:
        return MAX_SCORE + (ttl - 5) * free_extrems
    elif free_extrems == 2 and ttl >= 4:
        return MAX_SCORE - 1
    elif ttl > 0:
        return ttl * free_extrems
    else:
        return 0

def tile_value(board, x, y, stone_color):
    ttl_tile = 0
    score_tile = nb_in_line(board, x, y, 1, 1, stone_color)
    if score_tile >= MAX_SCORE - 10:
        return MAX_SCORE
    ttl_tile += score_tile
    score_tile = nb_in_line(board, x, y, 0, 1, stone_color)
    if score_tile >= MAX_SCORE - 10:
        return MAX_SCORE
    ttl_tile += score_tile
    score_tile = nb_in_line(board, x, y, 1, 0, stone_color)
    if score_tile >= MAX_SCORE - 10:
        return MAX_SCORE
    ttl_tile += score_tile
    score_tile = nb_in_line(board, x, y, 1, -1, stone_color)
    if score_tile >= MAX_SCORE - 10:
        return MAX_SCORE
    ttl_tile += score_tile
    return ttl_tile

# def heuristic_evaluation(board, board_array, player, winner, x, y, DRAW, depth):
#     if winner is not None:
#         if winner == DRAW:
#             return 0
#         return MAX_SCORE
#     player_score = player.peer_captured ** 2
#     enemy_score = 0

#     tile = player.stone_color

#     # for x in range(board._size):
#     #     for y in range(board._size):
#     if player.stone_color == tile:
#         tile_score = tile_value(board_array, x, y, player.stone_color)
#         if tile_score >= MAX_SCORE - 10:
#             return tile_score
#         else:
#             player_score += tile_score
#     elif -player.stone_color == tile:
#         tile_score = tile_value(board_array, x, y, -player.stone_color)
#         if tile_score >= MAX_SCORE - 10:
#             return tile_score
#         if tile_score == MAX_SCORE:
#             return -float('inf')
#         else:
#             enemy_score += tile_score

#     return player_score - enemy_score