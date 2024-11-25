from tkinter import Button, PhotoImage
from srcs.render.render_init import render
from srcs.backend.game.game_manager import game_manager as game_manager_module
from srcs.render.game_page_srcs.board_render import board_game
from srcs.render.game_page_srcs.best_move import create_best_move

PLAYER1_TEXT = {'x': 12.0, 'y': 97.0, 'font': ("Jaini Regular", 40, "bold italic")}
PLAYER2_TEXT = {'x': 802.0, 'y': 97.0, 'font': ("Jaini Regular", 40, "bold italic")}
PLAYER1_PEER_CAPTURED = {'x': 12.0, 'y': 192.0, 'font': ("Jaini Regular", 15, "bold italic")}
PLAYER2_PEER_CAPTURED = {'x': 802.0, 'y': 192.0, 'font': ("Jaini Regular", 15, "bold italic")}
PLAYER1_TIME_TEXT = {'x': 55.0, 'y': 249.0, 'font': ("Jaini Regular", 15, "bold italic")}
PLAYER2_TIME_TEXT = {'x': 845.0, 'y': 249.0, 'font': ("Jaini Regular", 15, "bold italic")}
TURN_TEXT = {'x': 400.0, 'y': 18.0, 'font': ("Jaini Regular", 50 * -1)}


def create_text_players(current_render : render, game_manager : game_manager_module):
    current_render.canvas.create_text(
        PLAYER1_TEXT['x'],
        PLAYER1_TEXT['y'],
        anchor="nw",
        text=game_manager.player1_name,
        fill="#000000",
        font=PLAYER1_TEXT['font']
    )

    current_render.canvas.create_text(
        PLAYER2_TEXT['x'],
        PLAYER2_TEXT['y'],
        anchor="nw",
        text=game_manager.player2_name,
        fill="#FFFFFF",
        font=PLAYER2_TEXT['font']
    )

def create_stone_text(current_render : render, game_manager : game_manager_module):
    current_render.player1_captured = current_render.canvas.create_text(
        PLAYER1_PEER_CAPTURED['x'],
        PLAYER1_PEER_CAPTURED['y'],
        anchor="nw",
        text=f"Peer Captured = {game_manager.player1_captured}",
        fill="#000000",
        font=PLAYER1_PEER_CAPTURED['font']
    )

    current_render.player2_captured = current_render.canvas.create_text(
        PLAYER2_PEER_CAPTURED['x'],
        PLAYER2_PEER_CAPTURED['y'],
        anchor="nw",
        text=f"Peer Captured = {game_manager.player2_captured}",
        fill="#FFFFFF",
        font=PLAYER2_PEER_CAPTURED['font']
    )
    
def create_time_text(current_render : render):
    current_render.player1_time = current_render.canvas.create_text(
        PLAYER1_TIME_TEXT['x'],
        PLAYER1_TIME_TEXT['y'],
        anchor="nw",
        text=f"00:00",
        fill="#000000",
        font=PLAYER1_TIME_TEXT['font']
    )

    current_render.player2_time = current_render.canvas.create_text(
        PLAYER2_TIME_TEXT['x'],
        PLAYER2_TIME_TEXT['y'],
        anchor="nw",
        text=f"00:00",
        fill="#FFFFFF",
        font=PLAYER2_TIME_TEXT['font']
    )
    
def create_turns_text(current_render : render, game_manager : game_manager_module):
    current_render.turn = current_render.canvas.create_text(
    TURN_TEXT['x'],
    TURN_TEXT['y'],
    anchor="nw",
    text=f"Turn N° {game_manager.turn:02d}",
    fill="#000000",
    font=TURN_TEXT['font']
)

def back_button(current_render : render):
    from srcs.render.main_page import render_main_page
    button_image_2 = PhotoImage(
        file=current_render.get_image("commun", "back"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: render_main_page(current_render),
        relief="flat"
    )
    button_2.place(
        x=12.0,
        y=11.0,
        width=43.0,
        height=44.0
    )

    button_image_hover_2 = PhotoImage(
        file=current_render.get_image("commun", "hover_back"))

    def button_2_hover(e):
        button_2.config(
            image=button_image_hover_2
        )
    def button_2_leave(e):
        button_2.config(
            image=button_image_2
        )

    button_2.bind('<Enter>', button_2_hover)
    button_2.bind('<Leave>', button_2_leave)

def render_Game_page(current_render : render, AI=False):
    game_manager = game_manager_module(current_render._settings, AI)
    print(game_manager.player.Ai._difficulty)
    current_render.clear_window()
    current_render.set_canvas()
    current_render.canvas.place(x = 0, y = 0)
    current_render.set_backgroud()
    create_turns_text(current_render, game_manager)
    create_text_players(current_render, game_manager)
    create_stone_text(current_render, game_manager)
    create_time_text(current_render)
    if not AI:
        create_best_move(current_render, game_manager)
    board_game(current_render, game_manager, AI)
    back_button(current_render)
