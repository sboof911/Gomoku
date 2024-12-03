import math
MAX_SCORE = 1000

def check_index(size, x, y):
    if x < 0 or y < 0:
        return False
    if x >= size or y >= size:
        return False
    return True

def evaluate(board_array, dx, dy, nx, ny, stone_color, connect_num, inverse=1):
    stone_number = 1
    free_extrems = 0
    blank = 0
    while check_index(board_array.shape[0], nx, ny) and board_array[ny][nx] == stone_color:
        nx += inverse*dx
        ny += inverse*dy
        stone_number += 1
    if check_index(board_array.shape[0], nx, ny) and board_array[ny][nx] != -stone_color:
        free_extrems += 1
        while check_index(board_array.shape[0], nx, ny) and board_array[ny][nx] == 0 and blank + stone_number < connect_num+1:
            nx += inverse*dx
            ny += inverse*dy
            blank += 1

    return stone_number, free_extrems, blank

def evaluate_pos(board_array, player, x_value, y_value, connect_num):
    score = 0
    directions = [(1, 1), (0, 1), (1, 0), (1, -1)]

    for dx, dy in directions:
        nx, ny = x_value + dx, y_value + dy
        stone_number, free_extrems, blank = evaluate(board_array, dx, dy, nx, ny, player.stone_color, connect_num)

        nx, ny = x_value - dx, y_value - dy
        tmp_stone_number, tmp_free_extrems, tmp_blank = evaluate(board_array, dx, dy, nx, ny, player.stone_color, connect_num, -1)
        stone_number += tmp_stone_number-1
        free_extrems += tmp_free_extrems
        blank += tmp_blank        

        if blank + stone_number < connect_num:
            pass
        elif stone_number >= connect_num:
            return MAX_SCORE
        elif free_extrems == 2 and stone_number == connect_num-1:
            return MAX_SCORE//2
        elif stone_number > 0:
            score += stone_number * free_extrems

    return score

def heuristic_evaluation(board_array, used_actions, players, current_player_index, connect_num):
    player = players[current_player_index]
    enemy_player = players[(current_player_index+1)%2]
    if player.peer_captured == player._max_peer_capture:
        return MAX_SCORE
    if enemy_player.peer_captured == player._max_peer_capture:
        return -(MAX_SCORE)
    player_score = player.peer_captured * 10
    enemy_player_score = enemy_player.peer_captured * 10

    if len(used_actions) == board_array.size:
        return player.DRAW

    for x, y in used_actions:
        if board_array[y][x] == player.stone_color:
            score = evaluate_pos(board_array, player, x, y, connect_num)
            if score == MAX_SCORE:
                return score
            player_score += score
        elif board_array[y][x] == enemy_player.stone_color:
            score = evaluate_pos(board_array, enemy_player, x, y, connect_num)
            if score == MAX_SCORE:
                return -score
            enemy_player_score += score


    total_score = player_score - enemy_player_score
    return (MAX_SCORE * math.copysign(1, total_score))-1 if abs(total_score) > MAX_SCORE else total_score
