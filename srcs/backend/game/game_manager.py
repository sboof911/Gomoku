from srcs.backend.game.board import board
from srcs.backend.game.player import player

class game_manager:
    def __init__(self, mode) -> None:
        self._board = board()
        self._player = player()

    def set_move(self, x, y):
        player_turn = self._player.player_turn
        if self._board.set_move(x, y, player_turn):
            self._player.change_turn()
            return True
        
        return False

    @property
    def board(self):
        return self._board._board
    
    @property
    def player_turn(self):
        return self._player._player_turn