from srcs.backend.game.board import board
from srcs.backend.game.player import player

class Game_Status:
    PLAYING = -1
    WINNER = None
    BLACK_WIN = 1
    WHITE_WIN = 2
    DRAW = 0

    def __init__(self) -> None:
        self._status = self.PLAYING

    def set_status(self, status_num):
        if status_num == -1:
            self._status = self.PLAYING
        elif status_num == 0:
            self._status = self.DRAW
        else:
            self.WINNER = 1 if status_num == 1 else 2
            self._status = self.WINNER


class game_manager:
    def __init__(self, mode) -> None:
        self._board = board()
        self._player = player()
        self._game_status = Game_Status()

    def set_move(self, x, y):
        player_turn = self._player.player_turn
        if self._board.set_move(x-1, y-1, player_turn): # -1 for 0->19
            status, pos = self._board.check_winner()
            self._game_status.set_status(status)
            if self._game_status._status == self._game_status.WINNER:
                self._player.set_winner(status, pos)
            self._player.change_turn()
            return True

        return False

    @property
    def board(self):
        return self._board._board
    
    @property
    def player_turn(self):
        return self._player._player_turn
    
    @property
    def status(self):
        return self._game_status._status