import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox as tkmbox
import json
import os
import logging


class App(ctk.CTk):
    def __init__(self):
        ctk.CTk.__init__(self) #initialise the parent(create the window)

        """
        change the cwd to the data directory 
        (which is the one we actualy want to use most of the time)
        """
        self.data_dir=os.getcwd().replace("frontend","data")
        os.chdir(self.data_dir)

        logging.basicConfig(filename="logs/main.log",
                            format = "%(asctime)s - %(levelname)s - %(message)s",
                            level = logging.DEBUG)
        logging.info("logging started")


        """
        check if it is the first time the user has run the app
        if it is, run the setup
        if not, apply the data from their previous session
        """
        if os.path.exists("first_session"):
            self.first_run()
        else:
            self.load_previous_session()

        self.protocol("WM_DELETE_WINDOW",self.quitter)


    def first_run(self):
        os.remove("first_session") #remove the first session flag, so that this only runs once.

        self.save("usr/window_state.json",
                {
                    "win_size":(600,500),
                    "win_pos":(30,30),
                }
                )

        self.save("usr/app_prefs.json",
                {
                    "ask_to_quit":True,
                }
                )


        #finaly, load the data that has just been written
        self.load_previous_session()



    def load_previous_session(self):

        window_state=self.load("usr/window_state.json")
        print(window_state)
        self.geometry(f"{window_state["win_size"][0]}x{window_state["win_size"][1]}+{window_state["win_pos"][0]}+{window_state["win_pos"][1]}")
        print(self.winfo_width(), self.winfo_height())
        self.app_preferences=self.load("usr/app_prefs.json")

    def load(self, filepath):
        try:
            with open(filepath) as f:
                data = json.load(f)
        except FileNotFoundError as e:
            print(f"{filepath} File not found")
            data=None
        finally:
            return data

    def save(self, filepath, data):
        with open(filepath, 'w') as f:
            json.dump(data, f)

    def quitter(self):

        #if the setting is enabled, ask the user for quit confirmation
        if self.app_preferences["ask_to_quit"]:
            if not tkmbox.askyesno(title="Quit?",message="Are you sure you want to quit?\n(you can disable this message in settings)"):
                return #cancel and return to the app

        print(self.winfo_width()/1.5, self.winfo_height()/1.5)

        window_state={
            "win_size":[int(self.winfo_width()/1.5), int(self.winfo_height()/1.5)],
            "win_pos":[self.winfo_x(), self.winfo_y()]
        }
        print(window_state)
        self.save("usr/window_state.json",window_state)


        self.destroy()
            

if __name__ == "__main__":
    app = App()
    app.mainloop()