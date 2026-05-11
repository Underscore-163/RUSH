import customtkinter as ctk
import json
import backend.logger as logger
log=logger.get_main_logger()

class App(ctk.CTk):
    def __init__(self):
        ctk.CTk.__init__(self)

        with open("data/app_data/win_quit.json","r") as file:
            win_data = json.load(file)
            self.geometry(f"{win_data["size"]["width"]}x{win_data["size"]["height"]}+{win_data["position"]["x"]}+{win_data["position"]["y"]}")

        self.protocol("WM_DELETE_WINDOW", self.close)


    def close(self):
        log.info("closing")
        with open("data/app_data/win_quit.json","w") as file:
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


