from srcs.backend.game.rules.standard import standard
from srcs.backend.game.board import board

SUPPORTED_RULES = ["standard", "PRO", "SWAP"]

class rules:
    def __init__(self, board_module : board, rule = "standard") -> None:
        if rule not in SUPPORTED_RULES:
            raise Exception(f"rule {rule} not supported!")
        self._rule = globals()[rule]()
        self._board = board_module

    def double_tree(self, board_array, x, y, stone_color):
        connect_num = self._board._connect_num - 2
        board_array[y][x] = stone_color
        count = 1 if self._board.check_horizontal(board_array, x, y, stone_color, connect_num)[0] else 0
        count += 1 if self._board.check_vertical(board_array, x, y, stone_color, connect_num)[0] else 0
        if count >= 2:
            return True
        count += 1 if self._board.check_Normal_diag(board_array, x, y, stone_color, connect_num)[0] else 0
        if count >= 2:
            return True
        count += 1 if self._board.check_Reversed_diag(board_array, x, y, stone_color, connect_num)[0] else 0

        return True if count >= 2 else False

    def is_legal(self, board_array, x, y, stone_color):
        #SUBJECT RULES
        if 0 <= x < self._board._size and 0 <= y < self._board._size:
            if self.double_tree(board_array.copy(), x, y, stone_color):
                print("Illegal move: Double three")
                return False
            #SPECIFIEDE RULES
            return self._rule.is_legal_move(board_array, x, y)
        return False
