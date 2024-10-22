from tkinter import Button, PhotoImage, Frame, Canvas
from srcs.render.render_init import render
from srcs.backend.game.game_manager import game_manager as game_manager_module

TABLE_MARGE = 14
MARGE_ERROR_THRESHOLD = 3

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

def draw_circle(canvas, x, y, color): #TODO: Change to an image or something
    radius = 5

    # The bounding box coordinates (top-left and bottom-right corners)
    x0, y0 = x - radius, y - radius
    x1, y1 = x + radius, y + radius

    # Draw the black disk
    canvas.create_oval(x0, y0, x1, y1, fill=color)

def draw_winning_line(canvas, pos, cell_width, cell_height, color):
    canvas.create_line(
        TABLE_MARGE + pos["x0"] * cell_width,
        TABLE_MARGE + pos["y0"] * cell_height,
        TABLE_MARGE + pos["x1"] * cell_width,
        TABLE_MARGE + pos["y1"] * cell_height,
        fill=color,
        width=2
        )

def board_click(event, game_manager : game_manager_module):
    canvas = event.widget
    
    # Get the width and height of the Canvas
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    cell_width = (canvas_width - (TABLE_MARGE * 2)) / 20
    cell_height = (canvas_height - (TABLE_MARGE * 2)) / 20
    x, y = event.x, event.y

    # Calculate the nearest grid lines (intersections)
    nearest_col = round((x - TABLE_MARGE) / cell_width)
    nearest_row = round((y - TABLE_MARGE) / cell_height)

    # Calculate the exact intersection coordinates
    intersection_x = TABLE_MARGE + nearest_col * cell_width
    intersection_y = TABLE_MARGE + nearest_row * cell_height

    # Check if the click is within ±2 pixels of the intersection
    if abs(x - intersection_x) <= MARGE_ERROR_THRESHOLD and abs(y - intersection_y) <= MARGE_ERROR_THRESHOLD:
        if game_manager.set_move(nearest_col, nearest_row):
            color = "black" if game_manager.player_turn != 1 else "white"
            draw_circle(canvas, intersection_x, intersection_y, color)
            if game_manager.status != game_manager._game_status.PLAYING:
                color = "black" if game_manager.status != 1 else "white"
                draw_winning_line(canvas,
                    game_manager._player._winner_pos,
                    cell_width,
                    cell_height,
                    color)
                print("black win" if game_manager.status == 1 else "white win")
                return True

    return False


def create_grid(canvas : Canvas, width, height, rows, cols):
    x = TABLE_MARGE
    y = TABLE_MARGE
    width = width - (x * 2)
    height = height - (y * 2)
    cell_width = width / cols
    cell_height = height / rows

    for i in range(rows + 1):
        canvas.create_line(x, y + i * cell_height, x + width, y + i * cell_height, fill="black")
    for j in range(cols + 1):
        canvas.create_line(x + j * cell_width, y, x + j * cell_width, y + height, fill="black")

def board_game(current_render : render, game_manager : game_manager_module):
    def clicked(event):
        if board_click(event, game_manager):
            from srcs.render.main_page import render_main_page
            print("Sleeping second before going back to main_menu!")
            current_render.window.after(10000, lambda: render_main_page(current_render))
            print("Back To main_menu") # TODO : Need to pop a two buttons(one for new game and the other one to go back to the main_menu) 

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

    canvas.bind("<Button-1>", clicked)

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
    game_manager = game_manager_module(mode)
    current_render.clear_window()
    current_render.set_canvas()
    current_render.canvas.place(x = 0, y = 0)
    current_render.set_backgroud()
    create_text_players(current_render, mode)
    board_game(current_render, game_manager)
    back_button(current_render)
