from srcs.backend.ai.ai_manager import Minimax

class player:
    BLACK = Minimax.BLACK
    WHITE = Minimax.WHITE
    DRAW = Minimax.DRAW
    ZERO = Minimax.ZERO
    AI_MODE = "AI"
    PLAYER_MODE = "Player"

    def __init__(self, name, stone_color, debug_mode=False, copy_mode=False) -> None:
        self.name = name
        self.stone_color = stone_color
        self.peer_captured = 0
        self._debug_mode = debug_mode
        if not copy_mode:
            self.Ai = Minimax(debug_mode=debug_mode)
        self.mode = self.PLAYER_MODE

    def set_mode(self , mode : str):
        if mode in [self.AI_MODE, self.PLAYER_MODE]:
            self.mode = mode
        else:
            raise ValueError("Invalid mode")

    def best_move(self, board, players, current_player_index):
        return self.Ai.get_best_move(board, players, current_player_index)
