from srcs.render.main_page import render_main_page
from srcs.render.render_init import render
from icecream import ic

def render_game(current_render : render):
    render_main_page(current_render)

def launch_game():
    try:
        current_render = render()
        render_game(current_render)
        current_render.canvas.addtag_all("all")
        current_render.window.mainloop()
    except Exception as error:
        ic('Oops!! :', error)