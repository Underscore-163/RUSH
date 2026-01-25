import customtkinter as ctk
from customtitlebar import CTT
from PIL import Image, ImageTk

class Titlebar(CTT):
    def __init__(self,master):
        CTT.__init__(self)

        self.icon=ctk.CTkImage(Image.open("assets/RUSH"))


test=CTT("dark")
ctk.CTkImage(Image.open("assets/RUSH"))
test.mainloop()