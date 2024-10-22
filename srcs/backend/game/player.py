

BLACK = 1
WHITE = 2

class player:
    def __init__(self) -> None:
        self._player_turn = BLACK
        self._winner_pos = (-1, -1)
        self._winner = None

    def change_turn(self):
        self._player_turn = BLACK if self._player_turn == WHITE else WHITE        

    def set_winner(self, winner, pos):
        self._winner = winner
        self._winner_pos = pos

    @property
    def player_turn(self):
        return self._player_turn
