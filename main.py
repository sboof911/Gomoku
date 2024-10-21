from srcs.render.main_page import render_main_page
from srcs.render.render_init import render


def render_game(current_render : render):
    img = render_main_page(current_render)
    return img

def lanch_game():
    current_render = render()
    img = render_game(current_render)
    current_render.canvas.addtag_all("all")
    current_render.window.mainloop()


if __name__ == "__main__":
    try:
        lanch_game()
    except Exception as e:
        print(f"Error: {e}")