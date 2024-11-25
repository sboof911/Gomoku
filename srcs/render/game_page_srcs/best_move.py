from tkinter import Button, PhotoImage
from srcs.render.render_init import render
from srcs.backend.game.game_manager import game_manager as game_manager_module

OFF_BLACK_BUTTON = {'x': 19.0, 'y': 301.0, 'width': 48.0, 'height': 48.0}
OFF_WHITE_BUTTON = {'x': 789.0, 'y': 311.0, 'width': 48.0, 'height': 48.0}
ON_BLACK_BUTTON = {'x': 19.0, 'y': 301.0, 'width': 48.0, 'height': 48.0}
ON_WHITE_BUTTON = {'x': 789.0, 'y': 311.0, 'width': 48.0, 'height': 48.0}
BLACK_BEST_MOVE = {'x': 91.0, 'y': 312.0, 'font': ("Jaini Regular", 20 * -1)}
WHITE_BEST_MOVE = {'x': 874.0, 'y': 320.0, 'font': ("Jaini Regular", 20 * -1)}

def best_move_black(current_render : render, game_manager : game_manager_module):
    if game_manager.current_player_index == 0:
        x, y = game_manager.best_move()
        x_var = chr(ord('A') + x)
        y_var = game_manager.size - y
    else:
        x_var = "X"
        y_var = "X"
    var = current_render.canvas.create_text(
        BLACK_BEST_MOVE['x'],
        BLACK_BEST_MOVE['y'],
        anchor="nw",
        text=f"{x_var}:{y_var}",
        fill="#FF7700",
        font=BLACK_BEST_MOVE['font']
    )
    current_render.best_move_text[str(0)] = var

def best_move_white(current_render : render, game_manager : game_manager_module):
    if game_manager.current_player_index == 1:
        x, y = game_manager.best_move()
        x_var = chr(ord('A') + x)
        y_var = game_manager.size - y
    else:
        x_var = "X"
        y_var = "X"
    var = current_render.canvas.create_text(
        WHITE_BEST_MOVE['x'],
        WHITE_BEST_MOVE['y'],
        anchor="nw",
        text=f"{x_var}:{y_var}",
        fill="#FF7700",
        font=WHITE_BEST_MOVE['font']
    )
    current_render.best_move_text[str(1)] = var

def off_black(current_render : render, game_manager : game_manager_module):
    game_manager.set_player_best_move(False, 0)
    current_render.canvas.delete(current_render.best_move_text[str(0)])
    current_render.best_move_text[str(0)] = None
    black_off_button = Button(
        image=current_render.off_buttons["black"],
        borderwidth=0,
        highlightthickness=0,
        command=lambda: on_black(current_render, game_manager),
        relief="flat"
    )
    black_off_button.place(**OFF_BLACK_BUTTON)

def off_white(current_render : render, game_manager : game_manager_module):
    game_manager.set_player_best_move(False, 1)
    current_render.canvas.delete(current_render.best_move_text[str(1)])
    current_render.best_move_text[str(1)] = None
    white_off_button = Button(
        image=current_render.off_buttons["white"],
        borderwidth=0,
        highlightthickness=0,
        command=lambda: on_white(current_render, game_manager),
        relief="flat"
    )
    white_off_button.place(**OFF_WHITE_BUTTON)

def on_black(current_render : render, game_manager : game_manager_module):
    game_manager.set_player_best_move(True, 0)
    best_move_black(current_render, game_manager)
    black_on_button = Button(
        image=current_render.on_buttons["black"],
        borderwidth=0,
        highlightthickness=0,
        command=lambda: off_black(current_render, game_manager),
        relief="flat"
    )
    black_on_button.place(**ON_BLACK_BUTTON)

def on_white(current_render : render, game_manager : game_manager_module):
    game_manager.set_player_best_move(True, 1)
    best_move_white(current_render, game_manager)
    white_on_button = Button(
        image=current_render.on_buttons["white"],
        borderwidth=0,
        highlightthickness=0,
        command=lambda: off_white(current_render, game_manager),
        relief="flat"
    )
    white_on_button.place(**ON_WHITE_BUTTON)

def create_best_move(current_render : render, game_manager : game_manager_module):
    current_render.off_buttons["black"] = PhotoImage(
    file=current_render.get_image("game_page", "off_black_button"))

    current_render.off_buttons["white"] = PhotoImage(
        file=current_render.get_image("game_page", "off_white_button"))

    current_render.on_buttons["black"] = PhotoImage(
        file=current_render.get_image("game_page", "on_black_button"))

    current_render.on_buttons["white"] = PhotoImage(
    file=current_render.get_image("game_page", "on_white_button"))

    off_black(current_render, game_manager)
    off_white(current_render, game_manager)
