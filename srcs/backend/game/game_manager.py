from srcs.backend.game.board import board
from srcs.backend.game.player import player
from srcs.backend.game.rules_manager import rules

class game_manager:
    def __init__(self, rule, board_size=19) -> None:
        self._board = board(board_size)
        self._players = []
        self._current_player_index = 0
        self._is_game_over = False
        self._rules = rules(rule) # need to check the settings class

    def add_player(self, player1, player2):
        self._players.append(player(player1, player.BLACK))
        self._players.append(player(player2, player.WHITE))

    def switch_turns(self):
        self._current_player_index = (self._current_player_index + 1) % 2

    def play_turn(self, x, y):
        current_player : player = self._players[self._current_player_index]
        if self._rules.is_legal(self.board, x, y):
            if self._board.place_stone(x-1, y-1, current_player.stone_color):
                if self._board.terminal_state():
                    self._is_game_over = True
                    print(f"Player {current_player.name} wins!")

                self.switch_turns()
                return True

        return False

    @property
    def player(self) -> player:
        return self._players[self._current_player_index]

    @property
    def board(self):
        return self._board._board

    @property
    def is_game_over(self):
        return self._is_game_over
    
    @property
    def line_pos_win(self):
        return self._board._line_pos
    
    @property
    def winner_color(self):
        return self._board._board_winner_color
