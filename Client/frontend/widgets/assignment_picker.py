import os
from tkinter import messagebox
import customtkinter as ctk
import tkinter.filedialog as filedialog
from Client.frontend.widgets.styles import Fonts
from Client.frontend.views.assignment_viewer import AssignmentViewer

class AssignmentPicker(ctk.CTkButton):
    def __init__(self,master,**kwargs):
        self.master=master
        self.fonts=Fonts()
        ctk.CTkButton.__init__(self,
                               self.master,
                               command=self.open_assignment,
                               text="Choose Assignment",
                               font=self.fonts.get_font(font="Medium",size=30,bold=True),
                               **kwargs)
        self.viewer=AssignmentViewer(self.master,"data/app_data/static/Select Assignment.rushzip")

    def open_assignment(self):
        filepath=filedialog.askopenfilename(defaultextension=".rush",
                                            initialdir=(os.getcwd()+"\\data\\user_data\\assignments"),
                                            filetypes=[("All RUSH assignment files",[".rush",".rushzip"]),
                                                       ("RUSH assignment file",".rush"),
                                                       ("RUSH zip assignment file",".rushzip"),
                                                       ("All Files","*.*")])
        try:
            self.viewer.pack_forget()
            self.viewer=AssignmentViewer(self.master,filepath)
            self.viewer.pack()
        except TypeError as e:
            messagebox.showwarning("Invalid Assignment File",str(e))

