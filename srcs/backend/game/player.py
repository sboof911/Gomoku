from srcs.backend.ai.ai_manager import AI_manager

class player:
    BLACK = AI_manager.BLACK
    WHITE = AI_manager.WHITE
    DRAW = AI_manager.DRAW
    ZERO = AI_manager.ZERO
    AI_MODE = "AI"
    PLAYER_MODE = "Player"

    def __init__(self, name, stone_color, debug_mode=False, copy_mode=False, peer_captured=0, mode=PLAYER_MODE) -> None:
        self.name = name
        self.stone_color = stone_color
        self.peer_captured = peer_captured
        self._debug_mode = debug_mode
        if not copy_mode:
            self.Ai = AI_manager(debug_mode=debug_mode)
        self.mode = mode

    def set_mode(self , mode : str):
        if mode in [self.AI_MODE, self.PLAYER_MODE]:
            self.mode = mode
        else:
            raise ValueError("Invalid mode")

    def best_move(self, board, players, current_player_index):
        return self.Ai.get_best_move(board, players, current_player_index)

    def clone(self):
        return player(self.name, self.stone_color, self._debug_mode,
                      copy_mode=True, peer_captured=self.peer_captured, mode=self.mode)