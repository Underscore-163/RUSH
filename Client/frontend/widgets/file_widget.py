import tkinter.messagebox

import customtkinter as ctk
from Client.frontend.widgets.styles import Fonts, Colours, Icons
from Client.frontend.widgets.combobutton import ComboButton
import subprocess
import os
import platform

class FileWidget(ctk.CTkFrame):
    def __init__(self,master,filepath,delete_permission=False):

        self.fonts = Fonts()
        self.colours = Colours()
        self.icons = Icons()

        self.filepath = filepath.replace("\\","/")

        filename_list = ((filepath.split("/")[-1]).split(".")[:-1])
        self.filename=filename_list[0]
        for section in filename_list[1:]:
            self.filename+="."+section

        self.file_extension = "."+filepath.split(".")[-1]

        self.master = master
        self.file_icon_path = "data/app_data/static/assets/file.png"
        self.folder_icon_path = "data/app_data/static/assets/folder.png"
        self.delete_permission = delete_permission

        ctk.CTkFrame.__init__(self,master=self.master)

        self.icon_label = ctk.CTkLabel(master=self,
                                       text="",
                                       image=ctk.CTkImage(self.icons.icon(self.file_icon_path, self.colours.primary),
                                                          size=(30, 30)))
        self.icon_label.pack(side="left",padx=10,pady=5)

        self.title_label = ctk.CTkLabel(master=self, text=self.filename, font=self.fonts.get_font("bold", 15))
        self.title_label.pack(side="left")

        self.control_button=ComboButton(master=self,
                                        title=self.file_extension,
                                        commands={
                                            "Open File": self.open_file,
                                            "Remove File": self.remove_file
                                        })
        self.control_button.pack(side="right", padx=5, pady=5, fill="y")

        self.update_width()

        self.bind("<Configure>", self.update_width)



    def open_file(self):

        # Source - https://stackoverflow.com/a/435669
        # Posted by Nick, modified by community. See post 'Timeline' for change history
        # Retrieved 2026-08-13, License - CC BY-SA 4.0
        # (Modified for this codebase)
        if platform.system() == 'Darwin':  # macOS
            subprocess.call(('open', self.filepath))
        elif platform.system() == 'Windows': # Windows
            os.startfile(self.filepath)
        else:  # linux variants
            subprocess.call(('xdg-open', self.filepath))

    def remove_file(self):
        if not self.delete_permission:
            tkinter.messagebox.showwarning(message="You are not allowed to remove this file.",title="No Permission")

    def update_width(self,*args):
        if len(self.filename)>=int((self.winfo_width())/20):
            self.title_label.configure(text=(self.filename[:int((self.winfo_width())/20)]+"..."))