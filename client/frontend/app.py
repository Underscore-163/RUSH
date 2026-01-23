import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox as tkmbox
import json
import os
from widgets.sidebar import Sidebar

os.chdir(os.getcwd().replace("frontend","data"))

from client.logger import logger

class App(ctk.CTk):
    def __init__(self):
        ctk.CTk.__init__(self) #initialise the parent(create the window)

        """
        change the cwd to the data directory 
        (which is the one we actualy want to use most of the time)
        """
        
        logger.info("=====Program started=====")

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
        self.bind("<Configure>", self.on_resize_event)

        self.navigator=Sidebar(master=self,width=200)




    def first_run(self):
        logger.info("Detected first session, running setup")
        os.remove("first_session") #remove the first session flag, so that this only runs once.

        self.save("usr/window_state.json",
                {
                    "win_size":(600,500),
                    "win_pos":(30,30),
                })

        self.save("usr/app_prefs.json",
                {
                    "ask_to_quit":True,
                })


        #finaly, load the data that has just been written
        self.load_previous_session()



    def load_previous_session(self):
        logger.info("Loading previous session")

        window_state=self.load("usr/window_state.json")
        self.geometry(f"{window_state["win_size"][0]}x{window_state["win_size"][1]}+{window_state["win_pos"][0]}+{window_state["win_pos"][1]}")
        self.app_preferences=self.load("usr/app_prefs.json")

    def load(self, filepath):
        if not os.path.isfile(filepath):
            logger.error(f"Failed to load {filepath}; Not a file.")
            return None
        try:
            with open(filepath) as f:
                data = json.load(f)
        except FileNotFoundError:
            logger.error(f"Failed to load {filepath}; File not found.")
            data=None
        except PermissionError:
            logger.error(f"Failed to load {filepath}; Permission Denied.")
            data=None
        except:
            logger.error(f"Failed to load {filepath}; Something went wrong.")
        finally:
            return data

    def save(self, filepath, data):
        with open(filepath, 'w') as f:
            json.dump(data, f)

    def on_resize_event(self,event):
        logger.debug(f"window resized to {event.width}x{event.height}")

    def quitter(self):

        #if the setting is enabled, ask the user for quit confirmation
        if self.app_preferences["ask_to_quit"]:
            if not tkmbox.askyesno(title="Quit?",message="Are you sure you want to quit?\n(you can disable this message in settings)"):
                return #cancel and return to the app

        logger.info("Quitting")

        window_state={
            "win_size":[int(self.winfo_width()/1.5), int(self.winfo_height()/1.5)],
            "win_pos":[self.winfo_x(), self.winfo_y()]
        }

        self.save("usr/window_state.json",window_state)


        self.destroy()
        logger.info("=====Program closed successfully=====")
            

if __name__ == "__main__":
    app = App()
    app.mainloop()