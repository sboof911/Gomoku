from srcs.backend.ai.ai_manager import ai_manager
# from srcs.backend.game.rules_manager import rules
# from srcs.backend.game.board import board

class player:
    BLACK = 1
    WHITE = -1
    DRAW = 2
    def __init__(self, name, stone_color):
        self.name = name
        self.stone_color = stone_color
        self._ai_manager = ai_manager(stone_color)

    def best_move(self, board, rules):
        return self._ai_manager.choose_move(board, rules)

