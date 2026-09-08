import customtkinter as ctk
from Client.frontend.widgets.styles import Fonts, Colours, Icons
import subprocess
import os
import platform

class FileWidget(ctk.CTkFrame):
    def __init__(self,master,filepath):

        self.fonts = Fonts()
        self.colours = Colours()
        self.icons = Icons()

        self.filepath = filepath
        self.filename = (filepath.split("\\")[-1])

        self.master = master
        self.file_icon_path = "data/app_data/static/assets/file.png"
        self.folder_icon_path = "data/app_data/static/assets/folder.png"

        ctk.CTkFrame.__init__(self,master=self.master)

        self.icon_label = ctk.CTkLabel(master=self,
                                       text="",
                                       image=ctk.CTkImage(self.icons.icon(self.file_icon_path, self.colours.primary),
                                                          size=(30, 30)))
        self.icon_label.pack(side="left",padx=10,pady=5)

        self.title_label=ctk.CTkLabel(master=self,text=self.filename,font=self.fonts.get_font("bold",15))
        self.title_label.pack(side="left")

        self.open_button=ctk.CTkButton(master=self,
                                       text="",
                                       command=self.open_file,
                                       width=15,
                                       height=15,
                                       image=ctk.CTkImage(self.icons.icon(self.folder_icon_path, self.colours.white),
                                                          size=(20, 20)))
        self.open_button.pack(side="right", padx=5,pady=5,fill="y")

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
