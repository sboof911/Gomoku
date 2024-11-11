from tkinter import Button, PhotoImage, Frame, Canvas
from srcs.render.render_init import render
from srcs.backend.game.game_manager import game_manager as game_manager_module

TABLE_MARGE = render.TABLE_MARGE
MARGE_ERROR_THRESHOLD = render.MARGE_ERROR_THRESHOLD

player1_text_x, player1_text_y = 10.0, 90.0
player2_text_x, player2_text_y = 487.0, 90.0

def create_text_players(current_render : render, player1_name, player2_name):
    current_render.canvas.create_text(
        player1_text_x,
        player1_text_y,
        anchor="nw",
        text=player1_name,
        fill="#1E1E1E",
        font=("Jaini Regular", 30 * -1)
    )

    

    current_render.canvas.create_text(
        player2_text_x,
        player2_text_y,
        anchor="nw",
        text=player2_name,
        fill="#FCF5F5",
        font=("Jaini Regular", 30 * -1)
    )

def update_captured_text(canvas_player1 : Canvas, canvas_player2 : Canvas, game_manager : game_manager_module):
    canvas_player1.delete("all")
    canvas_player2.delete("all")
    canvas_player1.create_text(
        0,
        0,
        anchor="nw",
        text=f"captured stones = {game_manager._players[0].peer_captured}",
        fill="#000000",
        font=("Jaini Regular", 10 * -1)
    )
    canvas_player2.create_text(
        0,
        0,
        anchor="nw",
        text=f"captured stones = {game_manager._players[1].peer_captured}",
        fill="#000000",
        font=("Jaini Regular", 10 * -1)
    )

def draw_circle(canvas : Canvas, x, y, color): #TODO: Change to an image or something
    radius = 5

    # The bounding box coordinates (top-left and bottom-right corners)
    x0, y0 = x - radius, y - radius
    x1, y1 = x + radius, y + radius

    # Draw the black disk
    canvas.create_oval(x0, y0, x1, y1, fill=color)

def draw_winning_line(canvas : Canvas, pos, cell_width, cell_height, color):
    canvas.create_line(
        (pos["x0"]+1) * cell_width,
        (pos["y0"]+1) * cell_height,
        (pos["x1"]+1) * cell_width,
        (pos["y1"]+1) * cell_height,
        fill=color,
        width=2
        )

def draw_player(game_manager : game_manager_module, canvas,
                x, y,cell_width, cell_height):
    intersection_x = (x+1) * cell_width
    intersection_y = (y+1) * cell_height
    color = "black" if game_manager.board[y][x] == game_manager.player.BLACK else "white"
    draw_circle(canvas, intersection_x, intersection_y, color)

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
        if game_manager.play_turn(nearest_col-1, nearest_row-1):
            return True

    return False

def check_winner(game_manager : game_manager_module, canvas : Canvas, cell_width, cell_height):
    # TODO : Need to pop a two buttons(one for new game and the other one to go back to the main_menu) 
    if game_manager.winner_color == game_manager.player.DRAW:
        print("draw")
    elif game_manager.line_pos_win is not None:
        print(f"Player {game_manager.player.name} wins")
        color = "black" if game_manager.winner_color != game_manager.player.BLACK else "white"
        draw_winning_line(canvas,
            game_manager.line_pos_win,
            cell_width,
            cell_height,
            color)
    else:
        print(f"Player {game_manager.player.name} wins with {game_manager.player.peer_captured} captured peer!")

def AI_playing(game_manager : game_manager_module):
    if game_manager.player.mode == game_manager.player.AI_MODE:
        x, y = game_manager.player.best_move(game_manager._board, game_manager._players, game_manager._current_player_index)
        game_manager.play_turn(x, y)

def board_game(current_render : render, game_manager : game_manager_module, Ai_mode):
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
    if Ai_mode:
        AI_playing(game_manager)
    draw_board(game_canvas, game_manager, board_img, cell_width, cell_height)

    ###########################################################
    # Captured frame/canvas
    text_width = 100
    text_height = 20
    texts_frame_player1 = Frame(current_render.window, borderwidth=0, highlightthickness=0, relief="flat")
    texts_frame_player1.pack()
    texts_frame_player1.place(x=player1_text_x, y=player1_text_y+30, width=text_width, height=text_height)
    texts_canvas_player1 = Canvas(texts_frame_player1, width=text_width, height=text_height, bg='white', highlightthickness=0)
    texts_canvas_player1.place(x=0, y=0)
    ##
    texts_frame_player2 = Frame(current_render.window, borderwidth=0, highlightthickness=0, relief="flat")
    texts_frame_player2.pack()
    texts_frame_player2.place(x=player2_text_x, y=player2_text_y+30, width=text_width, height=text_height)
    texts_canvas_player2 = Canvas(texts_frame_player2, width=text_width, height=text_height, bg='white', highlightthickness=0)
    texts_canvas_player2.place(x=0, y=0)

    update_captured_text(texts_canvas_player1, texts_canvas_player2, game_manager)

    def clicked(event):
        game_canvas.unbind("<Button-1>")

        if board_click(event, game_manager, cell_width, cell_height):
            draw_board(game_canvas, game_manager, board_img, cell_width, cell_height)
            update_captured_text(texts_canvas_player1, texts_canvas_player2, game_manager)
        if game_manager.is_game_over:
            check_winner(game_manager, game_canvas, cell_width, cell_height)
        elif Ai_mode:
            AI_playing(game_manager)
            draw_board(game_canvas, game_manager, board_img, cell_width, cell_height)
            if game_manager.is_game_over:
                check_winner(game_manager, game_canvas, cell_width, cell_height)

        if not game_manager.is_game_over:
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

def render_Game_page(current_render : render, AI=False):
    if AI:
        import random
        rnd_int = random.randint(0, 1)
        player1_name = "AI" if rnd_int == 1 else current_render._settings.player1
        player2_name = "AI" if rnd_int == 0 else current_render._settings.player1
    else:
        player1_name = current_render._settings.player1
        player2_name = current_render._settings.player2

    game_manager = game_manager_module(current_render._settings.rule)
    game_manager.add_player(player1_name, player2_name)
    for player in game_manager._players:
        if player.name == "AI":
            player.set_mode(player.AI_MODE)

    current_render.clear_window()
    current_render.set_canvas()
    current_render.canvas.place(x = 0, y = 0)
    current_render.set_backgroud()
    create_text_players(current_render, player1_name, player2_name)
    board_game(current_render, game_manager, AI)
    back_button(current_render)
