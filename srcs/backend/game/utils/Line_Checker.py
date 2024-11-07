import numpy as np

def get_line_pos(x0, y0, x1, y1):
    return dict(
        x0=x0+1,
        y0=y0+1,
        x1=x1+1,
        y1=y1+1
    )

def Horiz(board_array : np.ndarray, x, y, stone_color, connect_num):
    if 0 <= x < board_array.shape[1] and 0 <= y < board_array.shape[0]:
        if board_array[y][x] == stone_color:
            checker = board_array[y:y+connect_num, x]
            if np.all(checker == stone_color) and checker.size == connect_num:
                line_pos = get_line_pos(x, y, x, y+(connect_num-1))
                return line_pos
    return None

def Vertic(board_array : np.ndarray, x, y, stone_color, connect_num):
    if 0 <= x < board_array.shape[1] and 0 <= y < board_array.shape[0]:
        if board_array[y][x] == stone_color:
            checker = board_array[y, x:x+connect_num]
            if np.all(checker == stone_color) and checker.size == connect_num:
                line_pos = get_line_pos(x, y, x+(connect_num-1), y)
                return line_pos
    return None

def Diag(board_array : np.ndarray, x, y, stone_color, connect_num):
    if 0 <= x < board_array.shape[1] and 0 <= y < board_array.shape[0]:
        if board_array[y][x] == stone_color:
            checker = board_array[y:y+connect_num, x:x+connect_num]
            if np.all(np.diagonal(checker) == stone_color) and checker.shape == (connect_num, connect_num):
                line_pos = get_line_pos(x, y, x+(connect_num-1), y+(connect_num-1))
                return line_pos
    return None

def Reversed_Diag(board_array : np.ndarray, x, y, stone_color, connect_num):
    if 0 <= x < board_array.shape[1] and 0 <= y < board_array.shape[0]:
        if board_array[y][x] == stone_color:
            checker = board_array[y:y+connect_num, x-connect_num+1:x+1]
            if np.all(np.diagonal(np.fliplr(checker)) == stone_color) and checker.shape == (connect_num, connect_num):
                line_pos = get_line_pos(x, y, x-(connect_num-1), y+(connect_num-1))
                return line_pos
    return None