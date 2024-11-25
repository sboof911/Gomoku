from tkinter import Canvas, PhotoImage, Frame
from srcs.backend.game.game_manager import game_manager as game_manager_module
from srcs.render.game_page_srcs.drawing import draw_board, draw_indexs, draw_winning_line
from srcs.render.render_init import render
import time

TABLE_MARGE = render.TABLE_MARGE
MARGE_ERROR_THRESHOLD = render.MARGE_ERROR_THRESHOLD
BOARD_FRAME = {"x": 218.0, "y": 105.0, "width": 560.0, "height": 560.0}

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

def update_turn_text(current_render : render, game_manager : game_manager_module):
    current_render.canvas.itemconfig(
        current_render.turn,
        text=f"Turn N° {game_manager.turn:02d}"
    )

def update_captured_text(current_render : render, game_manager : game_manager_module):
    current_render.canvas.itemconfig(
        current_render.player1_captured,
        text=f"Peer Captured = {game_manager.player1_captured}"
    )
    current_render.canvas.itemconfig(
        current_render.player2_captured,
        text=f"Peer Captured = {game_manager.player2_captured}"
    )

def update_time_text(current_render : render, time_to_play, idx):
    # str_time = time.strftime("%S:%S", time.gmtime(time_to_play))
    # str_time = 
    print_time = f"{time_to_play:.2f}"
    find = print_time.find(".")
    str_time = f"{int(print_time[:find]):02d}:{print_time[find+1:]}"
    current_render.canvas.itemconfig(
        current_render.player1_time,
        text=str_time if idx == 0 else "00:00"
    )
    current_render.canvas.itemconfig(
        current_render.player2_time,
        text=str_time if idx == 1 else "00:00"
    )

def create_base_board(current_render : render, board_game_img, size):
    frame = Frame(current_render.window, borderwidth=0, highlightthickness=0, relief="flat")
    frame.pack()
    frame.place(**BOARD_FRAME)

    canvas = Canvas(frame, width=BOARD_FRAME['width'], height=BOARD_FRAME['height'], bg='white', highlightthickness=0)
    canvas.place(x=0, y=0)
    canvas.create_image(
            BOARD_FRAME["width"] / 2,
            BOARD_FRAME["height"] / 2,
            image=board_game_img)

    current_render.imgs.append(board_game_img)
    frame.update_idletasks()
    cell_width = (canvas.winfo_width() - (2*TABLE_MARGE)) / (size+1)
    cell_height = (canvas.winfo_height() - (2*TABLE_MARGE)) / (size+1)
    draw_indexs(canvas, cell_width, cell_height, TABLE_MARGE, size)

    return frame, canvas

def create_game(frame : Frame, canvas : Canvas,
                board_game_img,
                game_manager : game_manager_module):
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
    cell_width = game_canvas.winfo_width() / (game_manager.size+1)
    cell_height = game_canvas.winfo_height() / (game_manager.size+1)
    draw_board(game_canvas, game_manager, board_game_img, cell_width, cell_height)

    return cell_width, cell_height, game_canvas

def AI_playing(game_manager : game_manager_module):
    if game_manager.player.mode == game_manager.player.AI_MODE:
        x, y = game_manager.best_move()
        game_manager.play_turn(x, y)

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

def update_best_move(current_render : render, game_manager : game_manager_module, game_canvas):
    if game_manager.player.best_move_on:
        current_index = str(game_manager.current_player_index)
        next_index = str((game_manager.current_player_index+1)%2)
        x, y = game_manager.best_move()
        x_var = chr(ord('A') + x)
        y_var = game_manager.size - y
        current_render.canvas.itemconfig(
            current_render.best_move_text[current_index],
            text=f"{x_var}:{y_var}")
        current_render.canvas.itemconfig(
            current_render.best_move_text[next_index],
            text=f"X:X")
        game_canvas.update()


def launch_game(game_manager : game_manager_module, game_canvas : Canvas,
                current_render : render, board_img, cell_width,
                cell_height, Ai_mode):
    time_before_play = time.time()
    idx = 0
    def clicked(event):
        nonlocal time_before_play
        nonlocal idx
        game_canvas.unbind("<Button-1>")

        if board_click(event, game_manager, cell_width, cell_height):
            draw_board(game_canvas, game_manager, board_img, cell_width, cell_height)
            update_captured_text(current_render, game_manager)
            update_turn_text(current_render, game_manager)
            crr_time = time.time()
            update_time_text(current_render, crr_time - time_before_play, idx)
            idx = (idx + 1) % 2
            time_before_play = crr_time
            game_canvas.update()
            update_best_move(current_render, game_manager, game_canvas)
        if game_manager.is_game_over:
            check_winner(game_manager, game_canvas, cell_width, cell_height)
        elif Ai_mode:
            AI_playing(game_manager)
            draw_board(game_canvas, game_manager, board_img, cell_width, cell_height)
            update_captured_text(current_render, game_manager)
            update_turn_text(current_render, game_manager)
            crr_time = time.time()
            update_time_text(current_render, crr_time - time_before_play, idx)
            idx = (idx + 1) % 2
            time_before_play = crr_time
            if game_manager.is_game_over:
                check_winner(game_manager, game_canvas, cell_width, cell_height)

        if not game_manager.is_game_over:
            game_canvas.bind("<Button-1>", clicked)


    if game_manager.player.mode == game_manager.player.AI_MODE:
        AI_playing(game_manager)
        draw_board(game_canvas, game_manager, board_img, cell_width, cell_height)
        crr_time = time.time()
        update_time_text(current_render, crr_time - time_before_play, idx)
        idx = (idx + 1) % 2
        time_before_play = crr_time

    game_canvas.bind("<Button-1>", clicked)

def board_game(current_render : render, game_manager : game_manager_module, Ai_mode):
    board_game_img = PhotoImage(file=current_render.get_image("game_page", "board_game"))
    frame, canvas = create_base_board(current_render, board_game_img, game_manager.size)
    cell_width, cell_height, game_canvas = create_game(frame, canvas, board_game_img, game_manager)
    launch_game(game_manager, game_canvas, current_render, board_game_img, cell_width, cell_height, Ai_mode)
