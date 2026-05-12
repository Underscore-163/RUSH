import customtkinter as ctk
import json
from frontend.widgets.frames import ContentFrame
from frontend.widgets.fonts import Fonts
import backend.logger as logger
log=logger.get_main_logger()

class App(ctk.CTk):
    def __init__(self):
        ctk.CTk.__init__(self)

        with open("data/app_data/dynamic/win_quit.json","r") as file:
            win_data = json.load(file)
            self.geometry(f"{win_data["size"]["width"]}x{win_data["size"]["height"]}+{win_data["position"]["x"]}+{win_data["position"]["y"]}")

        fonts = Fonts()

        self.protocol("WM_DELETE_WINDOW", self.close)
        ctk.set_default_color_theme("data/app_data/static/assets/RUSH_theme.json")

        self.iconbitmap("data/app_data/static/assets/RUSH_icon.ico")
        test_frame=ContentFrame(self,title="Test",icon_path="./data/app_data/static/assets/RUSH_icon.png")
        test_frame.pack(fill="both",)



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


