from tkinter import Button, PhotoImage
from srcs.render.render_init import render
from srcs.render.game_page import render_Game_page
from srcs.render.settings_page import render_Settings_page


GAME_TITLE = {'x': 100.0, 'y': 30.0, 'font': ("JollyLodger", 85, "bold italic")}
SETTINGS_BUTTON = {'x': 884.0, 'y': 589.0, 'width': 80.0, 'height': 80.0}
PLAYER_AI_BUTTON = {'x': 182.0, 'y': 388.0, 'width': 641.0, 'height': 118.0}
PLAYER_PLAYER_BUTTON = {'x': 182.0, 'y': 232.0, 'width': 641.0, 'height': 118.0}


def game_Title(current_render : render):
    current_render.canvas.create_text(
        GAME_TITLE['x'],
        GAME_TITLE['y'],
        anchor="nw",
        text="Gomoku Game",
        fill="#0083FF",
        font=GAME_TITLE['font']
    )

def setting_button(current_render : render):
    button_image_1 = PhotoImage(
        file=current_render.get_image("main_page", "button_setting"))
    button_1 = Button(
        current_render.window,
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: render_Settings_page(current_render),
        relief="flat"
    )
    button_1.place(
        x=SETTINGS_BUTTON['x'],
        y=SETTINGS_BUTTON['y'],
        width=SETTINGS_BUTTON['width'],
        height=SETTINGS_BUTTON['height']
    )

    button_image_hover_1 = PhotoImage(
        file=current_render.get_image("main_page", "button_hover_setting"))

    def button_1_hover(e):
        button_1.config(
            image=button_image_hover_1
        )
    def button_1_leave(e):
        button_1.config(
            image=button_image_1
        )

    button_1.bind('<Enter>', button_1_hover)
    button_1.bind('<Leave>', button_1_leave)

def player_AI_button(current_render : render):
    button_image_2 = PhotoImage(
        file=current_render.get_image("main_page", "button_player_AI"))
    button_2 = Button(
        current_render.window,
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: render_Game_page(current_render, True),
        relief="flat"
    )
    button_2.place(
        x=PLAYER_AI_BUTTON['x'],
        y=PLAYER_AI_BUTTON['y'],
        width=PLAYER_AI_BUTTON['width'],
        height=PLAYER_AI_BUTTON['height']
    )

    button_image_hover_2 = PhotoImage(
        file=current_render.get_image("main_page", "button_hover_player_AI"))

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

def player_player_button(current_render : render):
    button_image_3 = PhotoImage(
        file=current_render.get_image("main_page", "button_player_player"))
    button_3 = Button(
        current_render.window,
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: render_Game_page(current_render),
        relief="flat"
    )
    button_3.place(
        x=PLAYER_PLAYER_BUTTON['x'],
        y=PLAYER_PLAYER_BUTTON['y'],
        width=PLAYER_PLAYER_BUTTON['width'],
        height=PLAYER_PLAYER_BUTTON['height']
    )

    button_image_hover_3 = PhotoImage(
        file=current_render.get_image("main_page", "button_hover_player_player"))

    def button_3_hover(e):
        button_3.config(
            image=button_image_hover_3
        )
    def button_3_leave(e):
        button_3.config(
            image=button_image_3
        )

    button_3.bind('<Enter>', button_3_hover)
    button_3.bind('<Leave>', button_3_leave)

def render_main_page(current_render : render):
    current_render.clear_window()
    current_render.set_canvas()
    current_render.canvas.place(x = 0, y = 0)
    current_render.set_backgroud()
    game_Title(current_render)
    setting_button(current_render)
    player_AI_button(current_render)
    player_player_button(current_render)
