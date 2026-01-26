import customtkinter as ctk
import tkinter as tk
from PIL import Image

class Sidebar:
    def __init__(self,master):
        self.master = master
        self.sidebar=ctk.CTkFrame(self.master,width=200)
        self.header=ctk.CTkFrame(self.sidebar, height=75)

        self.view=tk.IntVar(value=1)

        self.sidebar.pack(side="left", fill="y")
        self.header.pack()

        self.views = [
            Sidebar_Item(
            master=self.sidebar,
            sidebar=self,
            text="Home",
            image_path="data/assets/icons/fill/home.png",
            position=1,
            selection_var=self.view)
        ]

    def change_view(self):
        print("changed view to",self.view.get())
        for view in self.views:
            if view.position is not self.view.get():
                view.selected=False
            else:
                view.selected=True
                view.select()


class Sidebar_Item:
    def __init__(self,master, sidebar,text, image_path ,position, selection_var):
        self.master = master
        self.sidebar = sidebar
        self.text = text
        self.image = ctk.CTkImage(Image.open(image_path))
        self.position = position
        self.selection_var = selection_var
        self.selected=False

        self.frame = ctk.CTkFrame(self.master,
                                  fg_color="grey",
                                  bg_color="white",
                                  corner_radius=4)
        self.button=ctk.CTkButton(
            master=self.frame,
            command=self.clicked,
            text=self.text,
            image=self.image,
            anchor="w",
            fg_color="transparent",
        )

        self.frame.pack(fill="both", padx=5, pady=5)
        self.button.pack(fill="both",anchor="w")

    def clicked(self):
        self.selection_var.set(self.position)
        self.sidebar.change_view()

    def select(self):
        self.frame.configure(fg_color="#e97132")
