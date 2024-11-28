from srcs.game.board import board
from srcs.game.player import player
from srcs.settings.settings import settings

class game_manager:
    def __init__(self, settings : settings, AI_mode, board_size=19, connect_num=5) -> None:
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
        playersdata = {
            0:{
                "name": player1,
                "mode": player.PLAYER_MODE
            },
            1:{
                "name": player2,
                "mode": player2_mode
            }
        }
        idx = random.randint(0, 1)
        self._players.append(player(playersdata[idx]["name"],
                                    player.BLACK, settings.debug_mode,
                                    settings.difficulty_level,
                                    playersdata[idx]["mode"]))
        self._players.append(player(playersdata[(idx+1)%2]["name"],
                                    player.WHITE, settings.debug_mode,
                                    settings.difficulty_level,
                                    playersdata[(idx+1)%2]["mode"]))

    def switch_turns(self):
        self._current_player_index = (self._current_player_index + 1) % len(self._players)
        if self._current_player_index == 0:
            self._board.next_turn()

    def play_turn(self, x, y):
        current_player : player = self._players[self._current_player_index]
        played, self._board._board, _ = self._board.place_stone(x, y, self._players, self._current_player_index, debug=True)
        if played:
            self._board.set_used_actions()
            if self._board.terminal_state(x, y, current_player):
                self._is_game_over = True
                return True

            self.switch_turns()
            return True

        return False

    def best_move(self):
        return self.player.best_move(self._board, self._players, self._current_player_index)

    def set_player_best_move(self, best_move_on, idx):
        if idx != 0 and idx != 1:
            raise ValueError("Invalid player index")
        if not isinstance(best_move_on, bool):
            raise ValueError("Invalid best_move_on value")
        self._players[idx].best_move_on = best_move_on

    @property
    def current_player_index(self):
        return self._current_player_index

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

    @property
    def size(self):
        return self._board._size

    @property
    def player1_name(self):
        return self._players[0].name

    @property
    def player2_name(self):
        return self._players[1].name

    @property
    def player1_captured(self):
        return self._players[0].peer_captured

    @property
    def player2_captured(self):
        return self._players[1].peer_captured
    
    @property
    def turn(self):
        return self._board._turns