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
                position=0,
                selection_var=self.view),
            Sidebar_Item(
                master=self.sidebar,
                sidebar=self,
                text="classes",
                image_path="data/assets/icons/fill/home.png",
                position=1,
                selection_var=self.view),
        ]

        self.set_view(0)

    def change_view(self):
        print("changed view to",self.view.get())
        for view in self.views:
            if view.position is not self.view.get():
                view.deselect()
            else:
                view.select()

    def set_view(self,position):
        self.view.set(position)
        self.change_view()


class Sidebar_Item:
    def __init__(self,master, sidebar,text, image_path ,position, selection_var):
        self.master = master
        self.sidebar = sidebar
        self.root = self.sidebar.master
        self.text = text
        self.image = ctk.CTkImage(Image.open(image_path))
        self.position = position
        self.selection_var = selection_var

        self.button_frame = ctk.CTkFrame(self.master,
                                         fg_color="grey",
                                         bg_color="white",
                                         corner_radius=4)
        self.button=ctk.CTkButton(
            master=self.button_frame,
            command=self.clicked,
            text=self.text,
            image=self.image,
            anchor="w",
            fg_color="transparent",
        )

        self.button_frame.pack(fill="both", padx=5, pady=5)
        self.button.pack(fill="both",anchor="w")

        self.frame = ctk.CTkFrame(self.root,bg_color="transparent")

        ctk.CTkLabel(master=self.frame,text=self.position).pack()

    def clicked(self):
        self.selection_var.set(self.position)
        self.sidebar.change_view()

    def select(self):
        self.button_frame.configure(fg_color="#e97132")
        self.frame.pack(fill="both",expand=True)

    def deselect(self):
        self.button_frame.configure(fg_color="grey")
        self.frame.pack_forget()

