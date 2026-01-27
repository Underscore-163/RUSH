import customtkinter as ctk
from tkinter import messagebox as tkmbox
import os
from frontend.widgets.sidebar import Sidebar
from logger import get_main_logger
import utils

log= get_main_logger()


class App(ctk.CTk):
    def __init__(self):
        ctk.CTk.__init__(self) #initialise the parent(create the window)

        ctk.set_default_color_theme("data/assets/RUSH_theme.json")
        self.title("RUSH")
        self.iconbitmap("data/assets/RUSH_icon.ico")
        self.protocol("WM_DELETE_WINDOW",self.quitter)
        self.bind("<Configure>", self.on_resize_event)

        self.sidebar=Sidebar(master=self)


        """
        check if it is the first time the user has run the app
        if it is, run the setup
        if not, apply the data from their previous session
        """
        if os.path.exists("data/first_session"):
            self.first_run()
        else:
            self.load_previous_session()

        ctk.set_appearance_mode(self.app_preferences["appearance_mode"])



    def first_run(self):
        log.info("Detected first session, running setup")
        os.remove("data/first_session") #remove the first session flag, so that this only runs once.

        utils.save_json("data/usr/window_state.json",
                        {
                    "win_size":(600,500),
                    "win_pos":(30,30),
                    "sidebar_view_id":"home"
                })

        utils.save_json("data/usr/app_prefs.json",
                        {
                            "ask_to_quit":True,
                            "appearance_mode":"light",
                })

        #finaly, load the data that has just been written
        self.load_previous_session()



    def load_previous_session(self):
        log.info("Loading previous session")

        window_state=utils.load_json("data/usr/window_state.json")
        log.debug(f"window_state: {window_state}")
        self.geometry(f"{window_state["win_size"][0]}x{window_state["win_size"][1]}+{window_state["win_pos"][0]}+{window_state["win_pos"][1]}")
        self.sidebar_view_id=window_state["sidebar_view_id"]
        #self.title(f"RUSH - {self.sidebar_view_id.capitalize()}")

        self.app_preferences=utils.load_json("data/usr/app_prefs.json")




    def on_resize_event(self,event):
        #log.debug(f"window resized to {event.width}x{event.height}")
        if event.width<400:
            #self.navigator.collapse()
            pass


    def quitter(self):

        #if the setting is enabled, ask the user for quit confirmation
        if self.app_preferences["ask_to_quit"]:
            if not tkmbox.askyesno(title="Quit?",message="Are you sure you want to quit?\n(you can disable this message in settings)"):
                return #cancel and return to the app

        log.info("Quitting")

        window_state={
            "win_size":[int(self.winfo_width()/1.5), int(self.winfo_height()/1.5)],
            "win_pos":[self.winfo_x(), self.winfo_y()],
            "sidebar_view_id":self.sidebar_view_id,
        }

        utils.save_json("data/usr/window_state.json", window_state)


        self.destroy()

            

if __name__ == "__main__":
    app = App()
    app.mainloop()