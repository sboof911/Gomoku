from time import time
from srcs.ai.Minimax import minimax, MAX_SCORE, get_best_available_actions
from threading import Thread
from queue import Queue
from os import cpu_count, path
import pickle

MEMO_FILE = path.join(path.dirname(__file__), 'memo_cache', 'minimax_memo.pkl')
def load_memo():
    if path.exists(MEMO_FILE):
        with open(MEMO_FILE, 'rb') as f:
            return pickle.load(f)
    return {}

def save_memo(memo):
    with open(MEMO_FILE, 'wb') as f:
        pickle.dump(memo, f)

class AI_manager():
    BLACK = 1
    DRAW = MAX_SCORE**2
    WHITE = -1 * BLACK
    ZERO = 0 * BLACK

    def __init__(self, difficulty, debug_mode=False) -> None:
        self._difficulty = difficulty
        self._debug_mode = debug_mode
        self._ai_isThinking = False
        self._thread_num = cpu_count()

    def get_depth(self):
        if self._difficulty == 1:
            return 3
        elif self._difficulty == 2:
            return 7
        elif self._difficulty == 3:
            return 11
        raise Exception("Difficulty level not supported")

    def get_best_move(self, board, players, current_player_index):
        self._board = board
        self._depth = self.get_depth()
        self._players = players
        current_time = time()
        # x, y = self.launch_threads(current_player_index)
        if len(board._used_actions) == 0:
            center = self._board._size//2
            return center, center

        if not self._ai_isThinking:
            self._ai_isThinking = True
            players_clone = [player.clone() for player in players]
            memo = load_memo()
            _, x, y = minimax(board, board._board.copy(), self._depth,
                              players_clone, current_player_index,
                              used_actions=board._used_actions.copy(),
                              memo = memo)
            save_memo(memo)
            if x is None or y is None:
                x, y = get_best_available_actions(board._board, board._used_actions, self.ZERO)[0]
            self._ai_isThinking = False
        else:
            raise Exception("AI is already thinking")

        if self._debug_mode:
            print("Can't print the time, debug mode is on")
        else:
            print(f"Time to get best move:{time()-current_time:.2f}s")
        return x, y

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
                    "depth" : self._depth,
                    "players" : [player.clone() for player in self._players],
                    "current_player_index":current_player_index,
                    "queue_list":queue_list,
                    "available_actions":available_actions[start:end]
                }
                thread = Thread(target=minimax, kwargs=kwargs)
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