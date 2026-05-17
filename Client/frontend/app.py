import customtkinter as ctk
import json
import pywinstyles
import time
from frontend.widgets.frames import ContentFrame
from frontend.widgets.styles import Fonts, Colours
from frontend.widgets.combobutton import ComboButton
from frontend.widgets.sidebar import Sidebar
import backend.logger as logger
from performance_timer import PerformanceTimer

performance_timer = PerformanceTimer()

log=logger.get_main_logger()

class App(ctk.CTk):
    def __init__(self):
        performance_timer.lap("App class start")
        ctk.CTk.__init__(self)
        performance_timer.lap("CTk initialization")
        self.fonts = Fonts()
        self.colours= Colours()
        performance_timer.lap("app styles")



        pywinstyles.change_header_color(self,"#c04f15")
        pywinstyles.change_border_color(self,"#80350e")
        performance_timer.lap("pywinstyles")
        self.title("RUSH")
        self.iconbitmap("data/app_data/static/assets/RUSH_icon.ico")
        ctk.set_default_color_theme("data/app_data/static/assets/RUSH_theme.json")
        performance_timer.lap("title, icon, theme")

        self.protocol("WM_DELETE_WINDOW", self.close)


        with open("data/app_data/dynamic/win_quit.json","r") as file:
            win_data = json.load(file)
            self.geometry(f"{win_data["size"]["width"]}x{win_data["size"]["height"]}+{win_data["position"]["x"]}+{win_data["position"]["y"]}")
        performance_timer.lap("win_quit.json")

        self.sidebar=Sidebar(self)
        self.sidebar.pack()
        performance_timer.lap("sidebar creation")

        self.sidebar.add_view("Home","data/app_data/static/assets/home.png")
        self.sidebar.add_view("Settings","data/app_data/static/assets/settings.png")
        self.sidebar.add_view("3rd Option")
        performance_timer.lap("sidebar views")

        performance_timer.end(filter=True)



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
            json.dump(win_data,file)

        self.destroy()

def run():
    app = App()
    app.mainloop()
