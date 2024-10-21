from tkinter import Button, PhotoImage, Frame, Label, Canvas
from srcs.render.render_init import render


def create_text_players(current_render : render, mode):
    player1 = "Player 1" if mode == "players" else "Player"
    current_render.canvas.create_text(
        10.0,
        90.0,
        anchor="nw",
        text=player1,
        fill="#1E1E1E",
        font=("Jaini Regular", 30 * -1)
    )

    player2 = "Player 2" if mode == "players" else "AI"
    current_render.canvas.create_text(
        487.0,
        79.0,
        anchor="nw",
        text=player2,
        fill="#FCF5F5",
        font=("Jaini Regular", 30 * -1)
    )

def board_click(event):
    x, y = event.x, event.y
    print(f"Clicked at: (x={x}, y={y})")

def create_grid(canvas : Canvas, width, height, rows, cols):
    x = 14
    y = 14
    width = width - (x * 2)
    height = height - (y * 2)
    cell_width = width / cols
    cell_height = height / rows

    for i in range(rows + 1):
        canvas.create_line(x, y + i * cell_height, x + width, y + i * cell_height, fill="black")
    for j in range(cols + 1):
        canvas.create_line(x + j * cell_width, y, x + j * cell_width, y + height, fill="black")

def board_game(current_render : render):
    kwargs = dict(x=125.0, y=75.0, width=350.0, height=350.0)

    board_game_img = PhotoImage(file=current_render.get_image("game_page", "board_game"))
    frame = Frame(current_render.window, borderwidth=0, highlightthickness=0, relief="flat")
    frame.pack()
    frame.place(**kwargs)

    canvas = Canvas(frame, width=kwargs['width'], height=kwargs['height'], bg='white', highlightthickness=0)
    canvas.place(x=0, y=0)

    canvas.create_image(
            kwargs["width"] / 2,
            kwargs["height"] / 2,
            image=board_game_img)

    create_grid(canvas, rows=20, cols=20, width=kwargs["width"], height=kwargs["height"])

    canvas.bind("<Button-1>", board_click)
    
    current_render.save.append(board_game_img)

def back_button(current_render : render):
    from srcs.render.main_page import render_main_page
    button_image_2 = PhotoImage(
        file=current_render.get_image("game_page", "back"))
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
        file=current_render.get_image("game_page", "hover_back"))

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

def render_game_page(current_render : render, mode):
    current_render.clear_window()
    current_render.set_canvas()
    current_render.canvas.place(x = 0, y = 0)
    current_render.set_backgroud()
    create_text_players(current_render, mode)
    board_game(current_render)
    back_button(current_render)
