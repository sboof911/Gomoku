from srcs.backend.ai.ai_manager import Minimax

class player:
    BLACK = Minimax.BLACK
    WHITE = Minimax.WHITE
    DRAW = Minimax.DRAW
    ZERO = Minimax.ZERO
    def __init__(self, name, stone_color):
        self.name = name
        self.stone_color = stone_color

    def best_move(self, board, rules):
        Ai = Minimax(board, rules)
        return Ai.get_best_move(self.stone_color)
