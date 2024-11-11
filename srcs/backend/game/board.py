import numpy as np
from srcs.backend.game.player import player
from srcs.backend.game.rules_manager import rules

class board:
    def __init__(self, board_size, connect_num, rule) -> None:
        self._connect_num = connect_num
        self._size = board_size
        self._board = np.full((board_size, board_size), player.ZERO, dtype=int)
        self._board_winner_color = None
        self._line_pos = None
        self._rules = rules(self, rule)
        self._used_actions = set()
        
    def get_used_actions(self, board_array):
        used_actions = set()
        for x in range(self._size):
            for y in range(self._size):
                if board_array[y][x] != player.ZERO:
                    used_actions.add((x, y))
        return used_actions

    def set_used_actions(self):
        self._used_actions = self.get_used_actions(self._board)

    def get_Adjucents(self, x, y, connect_num=None):
        adjucents = {
            "Horizontal": [],
            "Vertical": [],
            "Normal_Diag": [],
            "Reversed_Diag": []
        }
        connect_num = self._connect_num if connect_num is None else connect_num
        if x is None and y is None:
            return adjucents

        for i in range(-connect_num+1, connect_num):
            index = y - i
            if 0 <= index < self._size:
                adjucents["Horizontal"].append((x, index))
            else:
                adjucents["Horizontal"].append((None, None))

            index = x - i
            if 0 <= index < self._size:
                adjucents["Vertical"].append((index, y))
            else:
                adjucents["Vertical"].append((None, None))

            index_x = x - i
            index_y = y - i
            if 0 <= index_x < self._size and 0 <= index_y < self._size:
                adjucents["Normal_Diag"].append((index_x, index_y))
            else:
                adjucents["Normal_Diag"].append((None, None))

            index_x = x + i
            index_y = y - i
            if 0 <= index_x < self._size and 0 <= index_y < self._size:
                adjucents["Reversed_Diag"].append((index_x, index_y))
            else:
                adjucents["Reversed_Diag"].append((None, None))

        return adjucents

    def check_capture(self, adjucents, players, board_array):
        player0_peer_captured = 0
        player1_peer_captured = 0
        def is_peer_captured(shape, array, key):
            help_array = []
            for x, y in array[key:len(shape)+key]:
                if x != None and y != None:
                    help_array.append(board_array[y][x])
                else:
                    break
            if len(shape) == len(help_array):
                if np.all(shape == help_array):
                    return True
            return False

        shape = [player.BLACK, player.WHITE, player.WHITE, player.BLACK]
        for direction in ["Horizontal", "Vertical", "Normal_Diag", "Reversed_Diag"]:
            for key, (x, y) in enumerate(adjucents[direction]):
                if x != None and y != None:
                    if board_array[y][x] != player.ZERO:
                        curr_shape = np.multiply(shape, -1) if board_array[y][x] < 0 else shape
                        if is_peer_captured(curr_shape, adjucents[direction], key):
                            captured_stone = player.ZERO
                            for i in range(1, len(shape)-1):
                                x0 = adjucents[direction][key+i][0]
                                y0 = adjucents[direction][key+i][1]
                                captured_stone = board_array[y0][x0]
                                board_array[y0][x0] = player.ZERO
                            if captured_stone != players[0].stone_color:
                                player0_peer_captured += 1
                            else:
                                player1_peer_captured += 1

        return board_array, player0_peer_captured, player1_peer_captured

    def place_stone(self, x, y, players, curr_player_index, board_array=None, debug=False):
        board_array = self._board if board_array is None else board_array
        adjucents = self.get_Adjucents(x, y)
        if self._rules.is_legal(board_array, adjucents, players[curr_player_index].stone_color, debug):
            board_array[y][x] = players[curr_player_index].stone_color
            board_array, peer0_captured, peer1_captured = self.check_capture(adjucents, players, board_array)
            players[0].peer_captured += peer0_captured
            players[1].peer_captured += peer1_captured
            return True, board_array

        return False, board_array

    def check_direction(self, stone_color, board_array, adjucents, direction, connect_num=None):
        connect_num = self._connect_num if connect_num is None else connect_num
        count = 0
        for key, (x, y) in enumerate(adjucents[direction]):
            if x != None and y != None:
                if board_array[y][x] == stone_color:
                    count += 1
                    if count == connect_num:
                        x0 = adjucents[direction][key-connect_num+1][0]
                        y0 = adjucents[direction][key-connect_num+1][1]
                        return True, dict(x0=x0, y0=y0, x1=x, y1=y)
                else:
                    count = 0

        return False, None

    def check_line_win(self, x, y, stone_color, board_array, set_winner):
        def check(line_pos):
            if set_winner:
                self._line_pos = line_pos
                self._board_winner_color = stone_color
            return True, stone_color

        adjucents = self.get_Adjucents(x, y)
        for direction in ["Horizontal", "Vertical", "Normal_Diag", "Reversed_Diag"]:
            is_win, line_pos = self.check_direction(stone_color, board_array, adjucents, direction)
            if is_win:
                return check(line_pos)

        return False, None

    def terminal_state(self, x, y, player : player, set_winner=True, board_array=None):
        if player.peer_captured >= 10:
            if set_winner:
                self._board_winner_color = player.stone_color
                return True
            return True, player.stone_color
        board_array = self._board if board_array is None else board_array
        line_win = self.check_line_win(x, y, player.stone_color, board_array, set_winner)
        if line_win[0]:
            if set_winner:
                return True
            return line_win

        if np.all(board_array != player.ZERO):
            if set_winner:
                self._board_winner_color = player.DRAW
                return True
            else:
                return True, player.DRAW

        return False if set_winner else (False, None)
