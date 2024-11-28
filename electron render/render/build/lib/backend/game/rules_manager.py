from backend.game.rules.standard import standard
from backend.game.player import player

SUPPORTED_RULES = ["standard", "PRO", "SWAP"]

class rules:
    def __init__(self, board_module, rule = "standard") -> None:
        from backend.game.board import board
        if rule not in SUPPORTED_RULES:
            raise Exception(f"rule {rule} not supported!")
        self._rule = globals()[rule]()
        self._board : board = board_module

    def double_tree(self, board_array, x, y, adjucents, stone_color):
        def check_line(directions, board_array):
            connect_num = (self._board._connect_num // 2)+1
            for key, direction in enumerate(directions):
                if self._board.check_direction(stone_color, board_array, adjucents, direction, connect_num)[0]:
                    return key+1
            return 0

        board_array[y][x] = stone_color
        directions = ["Horizontal", "Vertical", "Normal_Diag", "Reversed_Diag"]
        key = check_line(directions, board_array)
        if 0 < key < len(directions):
            if check_line(directions[key:], board_array):
                board_array[y][x] = player.ZERO
                return True
        board_array[y][x] = player.ZERO
        return False

    def is_legal(self, board_array, adjucents, stone_color, debug = False):
        #SUBJECT RULES
        pos = len(adjucents["Horizontal"]) // 2

        x = adjucents["Horizontal"][pos][0]
        y = adjucents["Horizontal"][pos][1]
        if x != None and y != None:
            if board_array[y][x] == player.ZERO:
                # if self.double_tree(board_array, x, y, adjucents, stone_color):
                #     if debug:
                #         print("Illegal move: Double three")
                #     return False
                #SPECIFIEDE RULES
                return self._rule.is_legal_move(board_array, x, y)
        return False
