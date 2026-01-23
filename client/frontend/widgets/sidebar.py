import customtkinter as ctk
from ctksidebar import CTkSidebarNavigation

class Sidebar(CTkSidebarNavigation):
    def __init__(self,master,width):
        self.master=master
        self.width=width
        CTkSidebarNavigation.__init__(self,master=self.master,width=self.width)

        self.pack(fill="both", expand=True)

        ##self.sidebar.add_frame(ctk.CTkLabel(self.sidebar,text="RUSH"))

    def collapse(self):
        print("collapse")

    def expand(self):
        print("expand")
