from srcs.backend.game.board import board
from srcs.backend.game.player import player
from srcs.backend.settings.settings import settings

class game_manager:
    def __init__(self, settings : settings, AI_mode, board_size=3, connect_num=3) -> None:
        self._board = board(board_size, connect_num, settings.rule)
        self._players = []
        self._current_player_index = 0
        self._is_game_over = False
        self.set_players(AI_mode, settings)

    def set_players(self, AI_mode, settings : settings):
        import random
        player1 = settings.player1
        player2 = settings.player2 if not AI_mode else settings.AIName
        player2_mode = player.AI_MODE if AI_mode else player.PLAYER_MODE
        idx = random.randint(0, 1)
        self._players.insert(idx, player(player1, player.BLACK, settings.debug_mode, settings.difficulty_level, player.PLAYER_MODE))
        self._players.insert((idx+1)%2, player(player2, player.WHITE, settings.debug_mode, settings.difficulty_level, player2_mode))

    def switch_turns(self):
        self._current_player_index = (self._current_player_index + 1) % len(self._players)
        if self._current_player_index == 0:
            self._board.next_turn()

    def play_turn(self, x, y):
        current_player : player = self._players[self._current_player_index]
        played, self._board._board = self._board.place_stone(x, y, self._players, self._current_player_index, debug=True)
        if played:
            self._board.set_used_actions()
            self._board.last_play = x, y
            if self._board.terminal_state(x, y, current_player):
                self._is_game_over = True
                return True

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
