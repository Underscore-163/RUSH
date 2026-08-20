import customtkinter as ctk
import json
import pywinstyles

from Client.frontend.widgets.styles import Fonts, Colours
from Client.frontend.widgets.sidebar import Sidebar
from Client.frontend.views.assignment_viewer import AssignmentViewer
from Client.backend import assignment_decoder
import Client.backend.logger as logger

log=logger.get_main_logger()

class App(ctk.CTk):
    def __init__(self):

        ctk.CTk.__init__(self)
        self.withdraw()

        self.fonts = Fonts()
        self.colours= Colours()

        self.protocol("WM_DELETE_WINDOW", self.close)

        pywinstyles.change_header_color(self, "#c04f15")
        pywinstyles.change_border_color(self, "#80350e")
        self.title("RUSH")
        self.iconbitmap("data/app_data/static/assets/RUSH_icon.ico")
        ctk.set_default_color_theme("data/app_data/static/assets/RUSH_theme.json")

        self.sidebar=Sidebar(self)
        self.sidebar.pack()

        self.sidebar.add_view("Home","data/app_data/static/assets/home.png")
        self.sidebar.add_view("Settings","data/app_data/static/assets/settings.png")
        self.sidebar.add_view("3rd Option")

        with open("data/app_data/dynamic/win_quit.json","r") as file:
            win_data = json.load(file)
            self.geometry(f"{win_data["size"]["width"]}x{win_data["size"]["height"]}+{win_data["position"]["x"]}+{win_data["position"]["y"]}")
            if win_data["maximised"]:
                self.state("zoomed")

        self.deiconify() #Show the window. Everything essential should be init'd before this.


        test_assign_viewer=AssignmentViewer(master=self.sidebar.get_frame("Home"),assignment=assignment_decoder.decode_assignment(r"data\user_data\assignments\test assignment.rush"))
        test_assign_viewer.pack()

        ctk.CTkButton(master=self.sidebar.get_frame("Settings"),command=lambda: self.state("normal")).pack()

    def close(self):
        log.info("closing")
        maximised=self.state()=="zoomed"
        if maximised:
            self.state("normal")
        with open("data/app_data/dynamic/win_quit.json","w") as file:
            win_data = {
                  "size":
                      {"width": int((self.winfo_width()/3)*2),
                       "height": int((self.winfo_height()/3)*2)},
                  "position":
                      {"x": self.winfo_x(),
                       "y": self.winfo_y()},
                  "maximised":maximised
                }
            json.dump(win_data,file)

        self.destroy()

def run():
    app = App()
    app.mainloop()
