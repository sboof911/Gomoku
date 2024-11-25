from tkinter import Button, PhotoImage, Entry
from srcs.render.render_init import render
from srcs.render.game_page import back_button

FONT = ("Jaini Regular", 30 * -1)
DIFFICULTY_TEXT = {"x":113.0, "y":422.0, "font":FONT}
NAMES_FIELD = {
    "Player1": {
        "Text": {"x":113.0, "y":102.0, "font":FONT},
        "Entry": {"x":363.0, "y":102.0, "font":FONT},
        "Error" : {"x":550.0, "y":102.0, "font":("Jaini Regular", 20 * -1)}
        },
    "Player2": {
        "Text": {"x":113.0, "y":206.0, "font":FONT},
        "Entry": {"x":363.0, "y":206.0, "font":FONT},
        "Error" : {"x":550.0, "y":206.0, "font":("Jaini Regular", 20 * -1)}
        },
    "AI_Player": {
        "Text": {"x":113.0, "y":310.0, "font":FONT},
        "Entry": {"x":363.0, "y":310.0, "font":FONT},
        "Error" : {"x":550.0, "y":310.0, "font":("Jaini Regular", 20 * -1)}
        }
}

DIFFUCLTY_BUTTON = {
    "Easy":{
        "On":{"x":325.0, "y":432.0, "width":24.0, "height":24.0},
        "Off":{"x":325.0, "y":432.0, "width":24.0, "height":24.0},
        "text":{"x": 360.0, "y": 422.0, "font": FONT}
        },
    "Medium":{
        "On":{"x":500.0, "y":432.0, "width":24.0, "height":24.0},
        "Off":{"x":500.0, "y":432.0, "width":24.0, "height":24.0},
        "text":{"x": 535.0, "y": 422.0, "font": FONT}
        },
    "Hard":{
        "On":{"x":692.0, "y":432.0, "width":24.0, "height":24.0},
        "Off":{"x":692.0, "y":432.0, "width":24.0, "height":24.0},
        "text":{"x": 727.0, "y": 422.0, "font": FONT}
        },
}

def create_Error_text(current_render : render, player, text : str):
    current_render.error_entries[player] = current_render.canvas.create_text(
        NAMES_FIELD[player]["Error"]["x"],
        NAMES_FIELD[player]["Error"]["y"],
        anchor="nw",
        text=text,
        fill="#F40000",
        font=NAMES_FIELD[player]["Error"]["font"]
    )

def create_text_player(current_render : render, player):
    current_render.canvas.create_text(
        NAMES_FIELD[player]["Text"]["x"],
        NAMES_FIELD[player]["Text"]["y"],
        anchor="nw",
        text=f"{player} Name :",
        fill="#000000",
        font=NAMES_FIELD[player]["Text"]["font"]
    )

def create_entry_player(current_render : render, player):
    player_entry = Entry(current_render.canvas, bd=0, highlightthickness=0,
                          relief='flat', width=8)
    player_name = player.lower()
    player_name = getattr(current_render, f"{player_name}_name")
    player_entry.insert(0, player_name)
    player_entry.config(font=NAMES_FIELD[player]["Entry"]["font"], fg="#000000", bg="#E0BB95")
    create_Error_text(current_render, player, "")

    def update_player1_name(event):
        try:
            current_render.player1_name = player_entry.get()
            if current_render.error_entries[player]:
                current_render.canvas.itemconfig(
                    current_render.error_entries[player],
                    text="")
            current_render.canvas.focus_set()
        except Exception as e:
            current_render.canvas.itemconfig(
                    current_render.error_entries[player],
                    text=f"{player} {e}")

    player_entry.bind('<Return>', update_player1_name)

    current_render.canvas.create_window(
        NAMES_FIELD[player]["Entry"]["x"],
        NAMES_FIELD[player]["Entry"]["y"],
        anchor="nw",
        window=player_entry
    )

def create_Players(current_render : render):
    players = ["Player1", "Player2", "AI_Player"]
    for player in players:
        create_text_player(current_render, player)
        create_entry_player(current_render, player)

def reset_difficulty_button(current_render : render, mode : str):
    modes = ["Easy", "Medium", "Hard"]
    mode_index = 1
    for key, m in enumerate(modes):
        if m != mode:
            create_button(current_render, m, False)
        else:
            mode_index = key+1

    return mode_index


def create_button(current_render : render, mode : str, off_on : bool):
    off_on_mode = "On" if off_on else "Off"
    if off_on:
        difficulty_index = reset_difficulty_button(current_render, mode)
        current_render.difficulty_level = difficulty_index

    button_image = PhotoImage(
    file=current_render.get_image("settings_page",f"{mode}_{off_on_mode}"))
    button_2 = Button(
        image=button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: create_button(current_render, mode, not off_on),
        relief="flat"
    )
    button_2.place(
        x=DIFFUCLTY_BUTTON[mode][off_on_mode]["x"],
        y=DIFFUCLTY_BUTTON[mode][off_on_mode]["y"],
        width=DIFFUCLTY_BUTTON[mode][off_on_mode]["width"],
        height=DIFFUCLTY_BUTTON[mode][off_on_mode]["height"]
    )

    current_render.imgs.append(button_image)

def create_Difficulty_texts(current_render : render):
    current_render.canvas.create_text(
        DIFFICULTY_TEXT['x'],
        DIFFICULTY_TEXT['y'],
        anchor="nw",
        text="Difficulty :",
        fill="#FFFFFF",
        font=DIFFICULTY_TEXT['font']
    )
    
    current_render.canvas.create_text(
        DIFFUCLTY_BUTTON["Easy"]["text"]['x'],
        DIFFUCLTY_BUTTON["Easy"]["text"]['y'],
        anchor="nw",
        text="Easy",
        fill="#000000",
        font=DIFFUCLTY_BUTTON["Easy"]["text"]['font']
    )
    
    current_render.canvas.create_text(
        DIFFUCLTY_BUTTON["Medium"]["text"]['x'],
        DIFFUCLTY_BUTTON["Medium"]["text"]['y'],
        anchor="nw",
        text="Medium",
        fill="#000000",
        font=DIFFUCLTY_BUTTON["Medium"]["text"]['font']
    )
    
    current_render.canvas.create_text(
        DIFFUCLTY_BUTTON["Hard"]["text"]['x'],
        DIFFUCLTY_BUTTON["Hard"]["text"]['y'],
        anchor="nw",
        text="Hard",
        fill="#000000",
        font=DIFFUCLTY_BUTTON["Hard"]["text"]['font']
    )

def create_Difficulty(current_render : render):
    create_Difficulty_texts(current_render)
    difficulties = ["Easy", "Medium", "Hard"]
    for key, difficulty in enumerate(difficulties):
        if key+1 == current_render.difficulty_level:
            create_button(current_render, difficulty, True)
        else:
            create_button(current_render, difficulty, False)

def render_Settings_page(current_render : render):
    current_render.clear_window()
    current_render.set_canvas()
    current_render.canvas.place(x = 0, y = 0)
    current_render.set_backgroud()
    create_Players(current_render)
    # create_Player2(current_render)
    # create_Player_AI(current_render)
    create_Difficulty(current_render)
    back_button(current_render)
