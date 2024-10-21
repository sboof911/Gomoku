from tkinter import BOTH, YES, Button, PhotoImage, Frame
from srcs.render.render_init import render

def backgroud(current_render : render):
    image_image_1 = PhotoImage(
        file=current_render.get_image("main_page", "backgroud"))
    current_render.canvas.create_image(
        300.0,
        250.0,
        image=image_image_1
    )

    current_render.canvas.create_text(
        47.0,
        38.0,
        anchor="nw",
        text="Gomoku Game",
        fill="#2E00FF",
        font=("IndieFlower Regular", 80 * -1)
    )
    return image_image_1

def setting_button(current_render : render):
    button_image_1 = PhotoImage(
        file=current_render.get_image("main_page", "button_setting"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("Setting button clicked"),
        relief="flat"
    )
    button_1.place(
        x=525.0,
        y=412.0,
        width=48.0,
        height=48.0
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
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("player vs AI button clicked"),
        relief="flat"
    )
    button_2.place(
        x=105.0,
        y=279.0,
        width=390.0,
        height=86.0
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
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("player vs player button clicked"),
        relief="flat"
    )
    button_3.place(
        x=104.0,
        y=164.0,
        width=390.0,
        height=86.0
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
    main_page_frame = Frame(current_render.window)
    main_page_frame.pack(fill=BOTH, expand=YES)
    current_render.set_canvas(main_page_frame)
    current_render.canvas.place(x = 0, y = 0)
    backgroud_image = backgroud(current_render)
    setting_button(current_render)
    player_AI_button(current_render)
    player_player_button(current_render)
    return backgroud_image
