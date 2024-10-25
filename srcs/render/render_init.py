import tkinter as tk
import os
from srcs.backend.settings.settings import settings
INIT_WIDTH = 600
INIT_HEIGHT = 500

class ResizingCanvas(tk.Canvas):
    def __init__(self,parent,**kwargs):
        self.save = []
        tk.Canvas.__init__(self,parent,**kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self,event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas 
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all",0,0,wscale,hscale)

class render:
    TABLE_MARGE = 14
    MARGE_ERROR_THRESHOLD = 3
    def __init__(self):
        self._window = tk.Tk()
        self._window.title("Gomoku")
        self._window.geometry(f"{INIT_WIDTH}x{INIT_HEIGHT}")
        self._window.resizable(True, True)
        self._canvas : tk.Canvas = None
        self._settings = settings()

    def get_image(self, page_name, image_name):
        current_folder = os.path.dirname(os.path.abspath(__file__))
        return f"{current_folder}/srcs/{page_name}/{image_name}_0.png" # TODO : change the 0 to the current settings

    def get_window_size(self):
        width = self._window.winfo_width() if self._window.winfo_width() > 1 else INIT_WIDTH
        height = self._window.winfo_height() if self._window.winfo_height() > 1 else INIT_HEIGHT

        return width, height

    def clear_window(self):
        self.save = []
        for widget in self._window.winfo_children():
            widget.pack_forget()

    def set_canvas(self, frame = None):
        window = self._window if frame is None else frame
        width, height = self.get_window_size() if frame is None else (window.winfo_width(), window.winfo_height())
        canvas = ResizingCanvas(
            window,
            bg = "#FFFFFF",
            height = height,
            width = width,
            bd = 0,
            highlightthickness = 0,
        )
        if frame is None:
            self._canvas = canvas
            self._canvas.pack(fill=tk.BOTH, expand=tk.YES)
        else:
            return canvas

    def set_backgroud(self):
        self._backgroud_img = tk.PhotoImage(
            file=self.get_image("backgrouds", "backgroud")) # need to get the backgroud from the settings
        self._canvas.create_image(
            300.0,
            250.0,
            image=self._backgroud_img
        )

    @property
    def window(self):
        return self._window

    @property
    def canvas(self):
        if self._canvas is None:
            raise Exception("canvas is empty!")

        return self._canvas

