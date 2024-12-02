from srcs.game.rules.standard import standard
from srcs.game.player import player

SUPPORTED_RULES = ["standard", "PRO", "SWAP"]

class rules:
    def __init__(self, board_module, rule = "standard") -> None:
        from srcs.game.board import board
        if rule not in SUPPORTED_RULES:
            raise Exception(f"rule {rule} not supported!")
        self._rule = globals()[rule]()
        self._board : board = board_module

    # def double_tree(self, board_array, x, y, adjucents, stone_color, pos):
        # def check_line(directions, board_array):
        #     connect_num = (self._board._connect_num // 2)+1
        #     for key, direction in enumerate(directions):
        #         is_alligned, pos = self._board.check_direction(stone_color, board_array, adjucents, direction, connect_num, True)
        #         if is_alligned:
        #             y0 = adjucents[direction][pos-connect_num][0]
        #             x0 = adjucents[direction][pos-connect_num][1]
        #             y1 = adjucents[direction][pos+1][0]
        #             x1 = adjucents[direction][pos+1][1]
        #             if board_array[y0][x0] == player.ZERO and board_array[y1][x1] == player.ZERO:
        #                 return key+1
        #     return 0

        # board_array[y][x] = stone_color
        # directions = ["Horizontal", "Vertical", "Normal_Diag", "Reversed_Diag"]
        # key = check_line(directions, board_array)
        # if 0 < key < len(directions):
        #     if check_line(directions[key:], board_array):
        #         board_array[y][x] = player.ZERO
        #         return True
        # board_array[y][x] = player.ZERO
        # return False

    def double_tree(self, board_array, adjucents_data, stone_color, x0, y0):
        def check_free_three(directions, adjucents):
            patterns = [
                [0, 1, 1, 1, 0],
                [0, 1, 0, 1, 1, 0],
                [0, 1, 1, 0, 1, 0]
            ]

            def match_pattern(line, pattern):
                for i in range(len(line) - len(pattern) + 1):
                    if all(line[i + j] == pattern[j] for j in range(len(pattern))):
                        return i
                return -1

            for direction in directions:
                line = []
                for x, y in adjucents[direction]:
                    if x is not None and y is not None:
                        line.append(board_array[y][x])
                    else:
                        line.append(-stone_color)

                for pattern in patterns:
                    key = match_pattern(line, pattern)
                    if key > -1:
                        return True, {"direction": direction, "start":key+1, "end":key+len(pattern)}

            return False, None

        board_array[y0][x0] = stone_color
        directions = ["Horizontal", "Vertical", "Normal_Diag", "Reversed_Diag"]
        found , data = check_free_three(directions, adjucents_data)
        if found:
            directions.remove(data["direction"])
            for key in range(data["start"], data["end"]):
                x = adjucents_data[data["direction"]][key][0]
                y = adjucents_data[data["direction"]][key][1]
                adjucents = self._board.get_Adjucents(x, y)
                if check_free_three(directions, adjucents)[0]:
                    board_array[y0][x0] = player.ZERO
                    return True

        board_array[y0][x0] = player.ZERO
        return False

    def is_legal(self, board_array, adjucents, stone_color, debug = False):
        #SUBJECT RULES
        pos = len(adjucents["Horizontal"]) // 2

        x = adjucents["Horizontal"][pos][0]
        y = adjucents["Horizontal"][pos][1]
        if x != None and y != None:
            if board_array[y][x] == player.ZERO:
                if self.double_tree(board_array, adjucents, stone_color, x, y):
                    if debug:
                        print("Illegal move: Double three")
                    return False
                #SPECIFIEDE RULES
                return self._rule.is_legal_move(board_array, x, y)
        return False
