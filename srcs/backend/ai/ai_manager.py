from time import time
from srcs.backend.ai.Minimax import negamax
from threading import Thread
from queue import Queue
from os import cpu_count

class AI_manager():
    BLACK = 1
    DRAW = 80 * BLACK
    WHITE = -1 * BLACK
    ZERO = 0 * BLACK

    def __init__(self, depth=4, debug_mode=False) -> None:
        self._depth = depth
        self._debug_mode = debug_mode
        self._thread_num = cpu_count()

    def get_best_move(self, board, players, current_player_index):
        self._board = board
        self._players = players
        current_time = time()

        # x, y = self.launch_threads(current_player_index)
        available_actions = self.get_available_actions()
        if len(available_actions) == 0:
            center = self._board._size//2
            return center, center
        _, x, y = negamax(board, board._board, self.get_depth(), players, current_player_index, available_actions=available_actions)
        if self._debug_mode:
            print("Can't print the time, debug mode is on")
        else:
            print(f"Time to get best move:{time()-current_time:.2f}s")
        return x, y

    def get_available_actions(self):
        used_actions = self._board.get_used_actions(self._board._board)
        if not used_actions:
            return []

        available_actions = []
        directions = ["Horizontal", "Vertical", "Normal_Diag", "Reversed_Diag"]
        x0, y0 = self._board.last_play
        available_actions_last_play = []
        for x, y in used_actions:
            adjucents = self._board.get_Adjucents(x, y, 2)
            for key in range(len(adjucents[directions[0]])):
                for direction in directions:
                    x1 = adjucents[direction][key][0]
                    y1 = adjucents[direction][key][1]
                    if x1 is not None and y1 is not None:
                        if self._board._board[y1][x1] == self.ZERO:
                            if (x1, y1) not in available_actions:
                                if x1 == x0 and y1 == y0:
                                    # available_actions_last_play.insert(0, (x1, y1))
                                    available_actions.insert(0, (x1, y1))
                                else:
                                    available_actions.append((x1, y1))

        # start = 0
        # actions_per_thread = len(available_actions) // self._thread_num
        # for x, y in available_actions_last_play:
        #     available_actions.remove((x, y))
        #     available_actions.insert(start, (x, y))
        #     start = start + actions_per_thread
        #     if start >= len(available_actions):
        #         start = 0

        return available_actions

    def get_depth(self):
        return self._depth
        depths = {
            "early": 3,
            "mid": 4,
            "late": 5
        }

        if self._board._turns < 3:
            return depths["early"]
        elif self._board._turns < 11:
            return depths["mid"]
        else:
            return depths["late"]

    def launch_threads(self, current_player_index):
        queue_list = Queue()
        threads = []

        available_actions = self.get_available_actions()
        if len(available_actions) == 0:
            center = self._board._size//2
            return center, center

        actions_per_thread = len(available_actions) // self._thread_num
        remainder = len(available_actions) % self._thread_num

        start = 0
        for i in range(self._thread_num):
            if start <= len(available_actions)-1:
                end = start + actions_per_thread + (1 if i < remainder else 0)
                kwargs = {
                    "board":self._board,
                    "board_array":self._board._board.copy(),
                    "depth" : self.get_depth(),
                    "players" : [player.clone() for player in self._players],
                    "current_player_index":current_player_index,
                    "queue_list":queue_list,
                    "available_actions":available_actions[start:end]
                }
                thread = Thread(target=negamax, kwargs=kwargs)
                threads.append(thread)
                thread.start()
                start = end

        for thread in threads:
            thread.join()

        best_move = (-1, -1)
        best_score = float('-inf')

        while not queue_list.empty():
            eval, x, y = queue_list.get()
            if eval > best_score:
                best_score = eval
                best_move = (x, y)

        if best_score == float('-inf'):
            from random import randint

            lostanyway = randint(0, len(available_actions)-1)
            if self._debug_mode:
                print("AI is lost anyway, random move")
            return available_actions[lostanyway][0], available_actions[lostanyway][1]

        return best_move