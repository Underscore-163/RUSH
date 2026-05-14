import customtkinter as ctk
import json
import pywinstyles
from PIL.ImageOps import expand
from frontend.widgets.frames import ContentFrame
from frontend.widgets.styles import Fonts, Colours
from frontend.widgets.combobutton import ComboButton
from frontend.widgets.sidebar import Sidebar
import backend.logger as logger
log=logger.get_main_logger()

class App(ctk.CTk):
    def __init__(self):
        ctk.CTk.__init__(self)
        self.fonts = Fonts()
        self.colours= Colours()

        pywinstyles.change_header_color(self,"#c04f15")
        pywinstyles.change_border_color(self,"#80350e")
        self.title("RUSH")
        self.iconbitmap("data/app_data/static/assets/RUSH_icon.ico")
        ctk.set_default_color_theme("data/app_data/static/assets/RUSH_theme.json")

        self.protocol("WM_DELETE_WINDOW", self.close)

        with open("data/app_data/dynamic/win_quit.json","r") as file:
            win_data = json.load(file)
            self.geometry(f"{win_data["size"]["width"]}x{win_data["size"]["height"]}+{win_data["position"]["x"]}+{win_data["position"]["y"]}")

        self.sidebar=Sidebar(self)
        self.sidebar.pack()

        self.sidebar.add_view("Home","data/app_data/static/assets/home.png")
        self.sidebar.add_view("Settings")
        self.sidebar.add_view("3rd Option")

        ctk.CTkButton(self.sidebar.get_frame("Home"),command=self.sidebar.collapse,text="Collapse").pack()
        ctk.CTkButton(self.sidebar.get_frame("Home"), command=self.sidebar.expand, text="Expand").pack()


    def close(self):
        log.info("closing")
        with open("data/app_data/dynamic/win_quit.json","w") as file:
            win_data = {
                  "size":
                      {"width": int((self.winfo_width()/3)*2),
                       "height": int((self.winfo_height()/3)*2)},
                  "position":
                      {"x": self.winfo_x(),
                       "y": self.winfo_y()}
                }
            log.debug(json.dumps(win_data))
            json.dump(win_data,file)

        self.destroy()

def run():
    app = App()
    app.mainloop()


def foo():
    print("foo")
def bar():
    print("bar")