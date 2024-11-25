from tkinter import Canvas
from srcs.backend.game.game_manager import game_manager as game_manager_module

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

def draw_indexs(canvas : Canvas, cell_width, cell_height, TABLE_MARGE):
    letters = [chr(ord('A') + i) for i in range(19)]
    for i, letter in enumerate(letters):
        x = TABLE_MARGE + cell_width * (i + 1)
        y = canvas.winfo_height() - cell_height / 2
        canvas.create_text(x, y, text=letter, fill="#FFFFFF")

    for i in range(19):
        x = cell_width / 2
        y = TABLE_MARGE + cell_height * (i + 1)
        canvas.create_text(x, y, text=str(19 - i), fill="#FFFFFF")