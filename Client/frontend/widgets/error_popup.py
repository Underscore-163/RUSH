import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import pywinstyles
import platform
import subprocess
import os
import webbrowser

class ErrorPopup(tk.Toplevel):
    def __init__(self,error,parent_window):
        #set up the window
        tk.Toplevel.__init__(self)
        self.geometry(f"650x400+{self.winfo_screenwidth()//2}+{self.winfo_screenheight()//2}")
        self.minsize(650,400)

        # if there is a parent window, set self as a child of the parent,
        # then forcefully take user input priority from the parent window.
        if parent_window is not None:
            self.transient(parent_window)
            self.grab_set()

        # set the styling
        pywinstyles.change_header_color(self, "#c04f15")
        pywinstyles.change_border_color(self, "#80350e")
        self.iconbitmap("data/app_data/static/assets/RUSH_icon.ico")

        self.focus_force()
        self.bell()

        self.title("RUSH Error Handler")

        self.error=error

        self.font = tk.font.Font(family="Arial", size=15)

        ttk.Label(self,
                  anchor="w",
                  font=self.font,
                  text="RUSH has encountered an error.\n\n"
                  ).pack(side="top",fill="x",padx=5,pady=5,anchor="w")
        ttk.Label(self,
                  anchor="w",
                  font=self.font,
                  text="RUSH should handle this gracefully without crashing, \nbut may fail to complete the action you were trying to do.\n"
                  ).pack(side="top", fill="x", padx=5, pady=5,anchor="w")
        ttk.Label(self,
                  anchor="w",
                  font=self.font,
                  text="If the issue persists, or RUSH crashes, please talk to your administrator."
                  ).pack(side="top", fill="x", padx=5, pady=5, anchor="w")

        self.text_box=tk.Text(self,relief="sunken",fg="#ff0000",width=10,height=5,)
        self.text_box.insert(index="1.0",chars=self.error)
        self.text_box.configure(state="disabled")
        self.text_box.pack(fill="both",expand=True)

        ttk.Button(self,text="Ok",command=lambda:self.destroy()).pack(side="left",padx=5,pady=5,anchor="w",expand=True,fill="both")
        ttk.Button(self, text="View Logs", command=lambda: self.open_logs()).pack(side="left",padx=5, pady=5, anchor="w",expand=True,fill="both")
        ttk.Button(self, text="Report Bug", command=lambda: self.report_bug()).pack(side="left",padx=5, pady=5, anchor="w",expand=True,fill="both")
        self.mainloop()

    def open_logs(self):
        filepath=os.getcwd()+"/data/logs/main.log"
        # Source - https://stackoverflow.com/a/435669
        # Posted by Nick, modified by community. See post 'Timeline' for change history
        # Retrieved 2026-08-13, License - CC BY-SA 4.0
        # (Modified for this codebase)
        if platform.system() == 'Darwin':  # macOS
            subprocess.call(('open', filepath))
        elif platform.system() == 'Windows':  # Windows
            os.startfile(filepath)
        else:  # linux variants
            subprocess.call(('xdg-open', filepath))

    def report_bug(self):
        webbrowser.open_new_tab("https://github.com/Underscore-163/RUSH/issues/new")

    def report_callback_exception(self, exc, val, tb):
        FatalErrorPopup("RUSH_ERROR_IN_HANDLER")

class FatalErrorPopup:
    def __init__(self,error_code="RUSH_FATAL_ERROR"):
        messagebox.showerror(
            title="Fatal Error",
            message=f"RUSH encountered an error that it couldn't recover from.\n\nError code: {error_code}")