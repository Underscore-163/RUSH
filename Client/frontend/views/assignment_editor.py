import tkinter as tk
import customtkinter as ctk
from Client.frontend.widgets.styles import Fonts, Colours, Icons
from Client.frontend.widgets.frames import ScrollableContentFrame, MDFrame, AttachmentsFrame

class AssignmentEditor(ctk.CTkScrollableFrame):
    def __init__(self,master,**kwargs):
        self.fonts=Fonts()
        self.colours=Colours()
        self.icons=Icons()
        ctk.CTkScrollableFrame.__init__(self,master=master,**kwargs)

        for i in range(2):
            self.columnconfigure(i,weight=1)
        self.rowconfigure(0,weight=5)
        self.rowconfigure(1, weight=0)


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
        self.settings_frame.grid(column=3,row=1,sticky="nsew",rowspan=2,pady=5,padx=5)

        ctk.CTkLabel(self,
                     text="Preview (may not be accurate)",
                     font=self.fonts.get_font("medium",10,True),
                     text_color=self.colours.dark_grey,
                     bg_color=self.colours.light_grey).grid(column=1,row=1,sticky="se",padx=10,pady=5)

        self.content_input.bind("<Key>",self.update_preview)

        self.attachments_frame=AttachmentsFrame(master=self)
        self.attachments_frame.grid(column=0,row=2,columnspan=2,sticky="nsew",pady=5,padx=5)



    def update_preview(self,event):
        if event.keycode==8:
            self.content_preview.update_md(self.content_input.get("1.0",tk.END)[:-2])
        else:
            self.content_preview.update_md(self.content_input.get("1.0",tk.END)[:-1]+event.char)

