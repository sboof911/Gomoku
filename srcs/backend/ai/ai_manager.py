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

    def __init__(self, depth=3, debug_mode=False) -> None:
        self._depth = depth
        self._debug_mode = debug_mode
        self._thread_num = cpu_count()

    def get_best_move(self, board, players, current_player_index):
        self._board = board
        self._players = players
        current_time = time()

        x, y = self.launch_threads(current_player_index)
        if self._debug_mode:
            print("Can't print the time, debug mode is on")
        else:
            print(f"Time to get best move:{time()-current_time:.2f}s")
        return x, y
    
    def get_available_actions(self):
        used_actions = self._board.get_used_actions(self._board._board)
        available_actions = set()
        directions = ["Horizontal", "Vertical", "Normal_Diag", "Reversed_Diag"]
        for x, y in used_actions:
            adjucents = self._board.get_Adjucents(x, y, 2)
            for key in range(len(adjucents[directions[0]])):
                for direction in directions:
                    x1 = adjucents[direction][key][0]
                    y1 = adjucents[direction][key][1]
                    if x1 is not None and y1 is not None:
                        if self._board._board[y1][x1] == self.ZERO:
                            available_actions.add((x1, y1))

        return list(available_actions)

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
                    "board_array":self._board._board,
                    "depth" : self._depth,
                    "players" : self._players,
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

        best_move = None
        best_score = float('-inf')

        while not queue_list.empty():
            eval, x, y = queue_list.get()
            if eval > best_score:
                best_score = eval
                best_move = (x, y)

        return best_move