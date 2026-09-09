import tkinter as tk
import customtkinter as ctk
from Client.frontend.widgets.styles import Fonts, Colours, Icons
from Client.frontend.widgets.frames import ScrollableContentFrame, MDFrame

class AssignmentEditor(ctk.CTkScrollableFrame):
    def __init__(self,master,**kwargs):
        self.fonts=Fonts()
        self.colours=Colours()
        self.icons=Icons()
        ctk.CTkScrollableFrame.__init__(self,master=master,**kwargs)

        for i in range(2):
            self.columnconfigure(i,weight=1)
        self.rowconfigure(0,weight=5)


        self.name_input=ctk.CTkEntry(master=self,height=30,placeholder_text="Assignment Name")
        self.content_input=ctk.CTkTextbox(master=self,
                                          border_color=self.colours.dark_grey,
                                          border_width=1,
                                          corner_radius=10,)
        self.content_preview=MDFrame(master=self,width=30)
        self.settings_frame=ctk.CTkFrame(master=self,)

        self.name_input.grid(column=0,row=0,sticky="nsew",columnspan=3,pady=5,padx=5)
        self.content_input.grid(column=0,row=1,sticky="nsew",padx=5)
        self.content_preview.grid(column=1,row=1,sticky="nsew",padx=5)
        self.settings_frame.grid(column=3,row=1,sticky="nsew")

        self.content_input.bind("<Key>",self.update_preview)

    def update_preview(self,event):
        if event.keycode==8:
            self.content_preview.update_md(self.content_input.get("1.0",tk.END)[:-2])
        else:
            self.content_preview.update_md(self.content_input.get("1.0",tk.END)[:-1]+event.char)

