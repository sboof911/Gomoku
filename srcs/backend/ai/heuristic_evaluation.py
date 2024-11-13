MAX_SCORE = 200

def evaluate(board, board_array, player, x_value, y_value):
        absulute_win = [0]
        for i in range(1, board._connect_num):
            absulute_win.append(1)
        absulute_win.append(0)

        directions = ["Horizontal", "Vertical", "Normal_Diag", "Reversed_Diag"]
        adjucents = board.get_Adjucents(x_value, y_value)
        score = 1

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

        return score*(player.peer_captured+1) if player.peer_captured > 0 else score

# def heuristic_evaluation(board, board_array, player, winner, x, y, DRAW, depth):
#     if winner == DRAW:
#         return 0
#     elif winner != None:
#         return MAX_SCORE*(depth+1)*player.stone_color

#     return evaluate(board, board_array, player, x, y)*player.stone_color




################################################################
WIN = float('inf') - 100

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
        return WIN + (ttl - 5) * free_extrems
    elif free_extrems == 2 and ttl >= 4:
        return WIN - 1
    elif ttl > 0:
        return ttl * free_extrems
    else:
        return 0

def tile_value(board, x, y, stone_color):
    ttl_tile = 0
    score_tile = nb_in_line(board, x, y, 1, 1, stone_color)
    if score_tile >= WIN - 10:
        return WIN
    ttl_tile += score_tile
    score_tile = nb_in_line(board, x, y, 0, 1, stone_color)
    if score_tile >= WIN - 10:
        return WIN
    ttl_tile += score_tile
    score_tile = nb_in_line(board, x, y, 1, 0, stone_color)
    if score_tile >= WIN - 10:
        return WIN
    ttl_tile += score_tile
    score_tile = nb_in_line(board, x, y, 1, -1, stone_color)
    if score_tile >= WIN - 10:
        return WIN
    ttl_tile += score_tile
    return ttl_tile

def heuristic_evaluation(board, board_array, player, winner, x, y, DRAW, depth):
    player_score = player.peer_captured ** 2
    enemy_score = 0

    tile = board_array[y][x]

    if player.stone_color == tile:
        tile_score = tile_value(board_array, x, y, player.stone_color)
        if tile_score >= WIN - 10:
            return tile_score
        else:
            player_score += tile_score
    elif -player.stone_color == tile:
        tile_score = tile_value(board_array, x, y, -player.stone_color)
        if tile_score >= WIN - 10:
            return tile_score
        if tile_score == WIN:
            return -float('inf')
        else:
            enemy_score += tile_score
    return player_score - enemy_score