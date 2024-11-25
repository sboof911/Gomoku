import tkinter as tk
import os
from srcs.backend.settings.settings import settings
INIT_WIDTH = 1000
INIT_HEIGHT = 700
IMAGE_DATA = {'x': 500.0, 'y': 350.0}

class save:
    def __init__(self):
        self.imgs = []
        self.player1_captured = None
        self.player2_captured = None
        self.player1_time = None
        self.player2_time = None
        self.turn = None
        
    def clear(self):
        self.imgs = []
        self.player1_captured = None
        self.player2_captured = None
        self.player1_time = None
        self.player2_time = None
        self.turn = None

class render(save):
    TABLE_MARGE = 22
    MARGE_ERROR_THRESHOLD = 5
    def __init__(self):
        self._window = tk.Tk()
        self._window.title("Gomoku")
        self._window.geometry(f"{INIT_WIDTH}x{INIT_HEIGHT}+0+0")
        self._window.resizable(False, False)
        self._canvas : tk.Canvas = None
        self._settings = settings()
        super().__init__()

    def get_image(self, page_name, image_name):
        current_folder = os.path.dirname(os.path.abspath(__file__))
        return f"{current_folder}/srcs/{page_name}/{image_name}_{self._settings._backgroud_img}.png"

    def clear_window(self):
        self.clear()
        for widget in self._window.winfo_children():
            widget.pack_forget()

    def set_canvas(self, frame = None):
        window = self._window if frame is None else frame
        canvas = tk.Canvas(
            window,
            bg = "#FFFFFF",
            height = INIT_HEIGHT,
            width = INIT_WIDTH,
            bd = 0,
            highlightthickness = 0,
        )
        self._canvas = canvas
        self._canvas.pack()

    def set_backgroud(self):
        backgroud_img = tk.PhotoImage(
            file=self.get_image("backgrouds", "backgroud")) # need to get the backgroud from the settings
        self._canvas.create_image(
            IMAGE_DATA['x'],
            IMAGE_DATA['y'],
            image=backgroud_img
        )
        self.imgs.append(backgroud_img)

    @property
    def window(self):
        return self._window

    @property
    def canvas(self):
        if self._canvas is None:
            raise Exception("canvas is empty!")

        return self._canvas

