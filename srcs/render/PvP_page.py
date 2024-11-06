from tkinter import Button, PhotoImage, Frame, Canvas
from srcs.render.render_init import render
from srcs.backend.game.game_manager import game_manager as game_manager_module

TABLE_MARGE = render.TABLE_MARGE
MARGE_ERROR_THRESHOLD = render.MARGE_ERROR_THRESHOLD

def create_text_players(current_render : render):
    current_render.canvas.create_text(
        10.0,
        90.0,
        anchor="nw",
        text=current_render._settings.player1,
        fill="#1E1E1E",
        font=("Jaini Regular", 30 * -1)
    )

    current_render.canvas.create_text(
        487.0,
        79.0,
        anchor="nw",
        text=current_render._settings.player2,
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
        pos["x0"] * cell_width,
        pos["y0"] * cell_height,
        pos["x1"] * cell_width,
        pos["y1"] * cell_height,
        fill=color,
        width=2
        )

def draw_player(game_manager : game_manager_module, canvas,
                x, y,cell_width, cell_height):
    intersection_x = (x+1) * cell_width
    intersection_y = (y+1) * cell_height
    color = "black" if game_manager.board[y][x] == game_manager.player.BLACK else "white"
    draw_circle(canvas, intersection_x, intersection_y, color)
    if game_manager.is_game_over:
        if game_manager.winner_color != game_manager.player.DRAW:
            color = "black" if game_manager.winner_color != game_manager.player.BLACK else "white"
            draw_winning_line(canvas,
                game_manager.line_pos_win,
                cell_width,
                cell_height,
                color)

def create_grid(canvas: Canvas, shape, cell_width, cell_height):
    for i in range(shape + 1):
        canvas.create_line(0, i * cell_height, shape * cell_width, i * cell_height, fill="black")
    for i in range(shape + 1):
        canvas.create_line(i * cell_width, 0, i * cell_height, shape * cell_height, fill="black")

def draw_board(canvas : Canvas, game_manager : game_manager_module,
               board_img, cell_width, cell_height):

    canvas.delete("all")
    canvas.create_image(
            canvas.winfo_width() / 2,
            canvas.winfo_height() / 2,
            image=board_img)

    create_grid(canvas, game_manager.board.shape[0]+1, cell_width, cell_height)
    for x in range(game_manager.board.shape[0]):
        for y in range(game_manager.board.shape[1]):
            if game_manager.board[y][x] != game_manager.player.ZERO:
                draw_player(game_manager, canvas, x, y, cell_width, cell_height)

def board_click(event, game_manager : game_manager_module,
                cell_width, cell_height):
    x, y = event.x, event.y
    # Calculate the nearest grid lines (intersections)
    nearest_col = round((x) / cell_width)
    nearest_row = round((y) / cell_height)
    # Calculate the exact intersection coordinates
    intersection_x = nearest_col * cell_width
    intersection_y = nearest_row * cell_height
    # Check if the click is within ±2 pixels of the intersection
    if abs(x - intersection_x) <= MARGE_ERROR_THRESHOLD and abs(y - intersection_y) <= MARGE_ERROR_THRESHOLD:
        if game_manager.play_turn(nearest_col, nearest_row):
            return True

    return False

def board_game(current_render : render, game_manager : game_manager_module):
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

    ###########################################################

    board_img = PhotoImage(file=current_render.get_image("game_page", "board_game"))
    frame.update_idletasks()
    game_frame = Frame(frame, borderwidth=0, highlightthickness=0, relief="flat")
    game_kwargs = dict(x=TABLE_MARGE,
                  y=TABLE_MARGE,
                  width=canvas.winfo_width() - (2*TABLE_MARGE),
                  height=canvas.winfo_height() - (2*TABLE_MARGE))
    game_frame.pack()
    game_frame.place(**game_kwargs)
    game_canvas = Canvas(game_frame, width=game_kwargs['width'], height=game_kwargs['height'], bg='white', highlightthickness=0)
    game_canvas.place(x=0, y=0)
    game_frame.update_idletasks()

    cell_width = game_canvas.winfo_width() / (game_manager.board.shape[0]+1)
    cell_height = game_canvas.winfo_height() / (game_manager.board.shape[0]+1)
    draw_board(game_canvas, game_manager, board_img, cell_width, cell_height)

    def clicked(event):
        game_canvas.unbind("<Button-1>")

        if board_click(event, game_manager, cell_width, cell_height):
            draw_board(game_canvas, game_manager, board_img, cell_width, cell_height)
        if game_manager.is_game_over:
            # TODO : Need to pop a two buttons(one for new game and the other one to go back to the main_menu) 
            if game_manager.winner_color == game_manager.player.DRAW:
                print("draw")
            else:
                print(f"Player {game_manager.player.name} wins!")
        else:
            game_canvas.bind("<Button-1>", clicked)

    game_canvas.bind("<Button-1>", clicked)

    current_render.save.append(board_game_img)
    current_render.save.append(board_img)

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

def render_PvP_page(current_render : render):
    game_manager = game_manager_module(current_render._settings.rule)
    game_manager.add_player(current_render._settings.player1,
                            current_render._settings.player2)
    current_render.clear_window()
    current_render.set_canvas()
    current_render.canvas.place(x = 0, y = 0)
    current_render.set_backgroud()
    create_text_players(current_render)
    board_game(current_render, game_manager)
    back_button(current_render)
