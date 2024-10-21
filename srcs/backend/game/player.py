

BLACK = 1
WHITE = 2

class player:
    def __init__(self) -> None:
        self._player_turn = BLACK
        self._winner = None

    def change_turn(self):
        self._player_turn = BLACK if self._player_turn == WHITE else WHITE

    @property
    def player_turn(self):
        return self._player_turn
    
    @property
    def game_status(self):
        return "playing" # "winner" "draw"