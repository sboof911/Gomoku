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

def heuristic_evaluation(board_array, player, x_value, y_value, connect_num):
        directions = [(1, 1), (0, 1), (1, 0), (1, -1)]
        if player.peer_captured == player._max_peer_capture:
            return MAX_SCORE + 10
        score = 0

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
                return MAX_SCORE + 10
            elif free_extrems == 2 and stone_number >= connect_num-1:
                return MAX_SCORE
            elif stone_number > 0:
                score += stone_number * free_extrems

        return score + (player.peer_captured * 10)
