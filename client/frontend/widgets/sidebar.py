import customtkinter as ctk
import tkinter as tk
from PIL import Image

class Sidebar:
    def __init__(self,master):
        self.master = master
        self.sidebar=ctk.CTkFrame(self.master,width=200,fg_color="lightgrey")
        self.header=Sidebar_Header(self)
        self.sidebar.pack_propagate(False)
        self.collapsed=False

        self.view=tk.IntVar(value=1)

        self.sidebar.pack(side="left", fill="y")


        self.views = [
            Sidebar_Item(
                master=self.sidebar,
                sidebar=self,
                text="Home",
                image_path="data/assets/icons/fill/home.png",
                position=0,
                selection_var=self.view),
            Sidebar_Menu(
                master=self.sidebar,
                sidebar=self,
                text="classes",
                image_path="data/assets/icons/fill/home.png",
                position=1,
                selection_var=self.view),
            Sidebar_Item(
                master=self.sidebar,
                sidebar=self,
                text="Settings",
                image_path="data/assets/icons/fill/home.png",
                position=3,
                selection_var=self.view)
        ]

        self.set_view(0)

        self.collapse_button=ctk.CTkButton(master=self.sidebar,
                                           text="",
                                           image=ctk.CTkImage(Image.open("data/assets/icons/fill/collapse.png")),
                                           command=self.collapse,
                                           width=40,
                                           height=40)
        self.collapse_button.pack(side="bottom", padx=5, pady=5, anchor="sw")

        self.expand_button = ctk.CTkButton(master=self.sidebar,
                                           text="",
                                           image=ctk.CTkImage(Image.open("data/assets/icons/fill/expand.png")),
                                           command=self.expand,
                                           width=40,
                                           height=40)

        ctk.CTkLabel(master=self.views[0].frame,text="",image=ctk.CTkImage(Image.open("data/assets/icons/line/home.png"),size=(16,16)),).pack()

    def change_view(self):
        print("changed view to",self.view.get())
        for view in self.views:
            print(f"view:{view.text}")
            if type(view)==Sidebar_Menu and not self.collapsed:
                for item in view.items:
                    print(f"item{item.text} in ")
                    if item.position is not self.view.get():
                        item.deselect()
                    else:
                        print(f"selected {view.text}")
                        item.select()
            elif type(view) == Sidebar_Menu and self.collapsed:
                if view.position is not self.view.get():
                    view.deselect()
                else:
                    view.select()
            else:
                if view.position is not self.view.get():
                    view.deselect()
                else:
                    view.select()



    def set_view(self,position):
        self.view.set(position)
        self.change_view()

    def collapse(self):
        self.sidebar.configure(width=50)
        self.header.collapse()
        for view in self.views:
            view.collapse()
        self.collapse_button.pack_forget()
        self.expand_button.pack(side="bottom", padx=5, pady=5, anchor="sw")
        self.collapsed=True

    def expand(self):
        self.sidebar.configure(width=200)
        self.header.expand()
        for view in self.views:
            view.expand()
        self.expand_button.pack_forget()
        self.collapse_button.pack(side="bottom", padx=5, pady=5, anchor="sw")
        self.collapsed=False



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
                                         fg_color="grey",)
        self.button=ctk.CTkButton(
            master=self.button_frame,
            command=self.clicked,
            text=self.text,
            image=self.image,
            anchor="w",
            fg_color="transparent",
            height=40,
        )

        self.button_frame.pack(fill="both", padx=5, pady=5)
        self.button.pack(fill="both",anchor="w")

        self.frame = ctk.CTkFrame(self.root,bg_color="transparent")

        ctk.CTkLabel(master=self.frame,text=self.position).pack()


    def clicked(self):
        self.selection_var.set(self.position)
        print(self.selection_var.get())
        self.sidebar.change_view()

    def select(self):
        self.button_frame.configure(fg_color="#e97132")
        self.frame.pack(fill="both",expand=True)
        print(self.text,"selected")

    def deselect(self):
        self.button_frame.configure(fg_color="grey")
        self.frame.pack_forget()

    def collapse(self):
        self.button.configure(text="")

    def expand(self):
        self.button.configure(text=self.text)


class Sidebar_Header:
    def __init__(self,sidebar):
        self.sidebar = sidebar
        self.frame = ctk.CTkFrame(self.sidebar.sidebar,fg_color="transparent")
        self.expanded_image=ctk.CTkImage(Image.open("data/assets/RUSH_logo.png"),size=(150,30))
        self.collapsed_image=ctk.CTkImage(Image.open("data/assets/RUSH_icon.png"),size=(30,30))

        self.image_label = ctk.CTkLabel(master=self.frame,image=self.expanded_image, text="")
        self.image_label.pack(padx=5,pady=10)
        self.frame.pack(fill="x")

    def collapse(self):
        self.image_label.configure(image=self.collapsed_image)
    def expand(self):
        self.image_label.configure(image=self.expanded_image)

class Sidebar_Menu(Sidebar_Item):
    def __init__(self,master, sidebar,text, image_path ,position, selection_var):
        self.master = master
        self.sidebar = sidebar
        self.root = self.sidebar.master
        self.text = text
        self.image = ctk.CTkImage(Image.open(image_path))
        self.position = position
        self.selection_var = selection_var
        self.open=False


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
            height=40
        )

        self.button_frame.pack(fill="both", padx=5, pady=5)
        self.button.pack(fill="both",anchor="w")

        self.menu_frame = ctk.CTkFrame(master=self.button_frame,)

        self.items=[
            Sidebar_Item(master=self.menu_frame,
                         sidebar=self.sidebar,
                         text="English",
                         image_path="data/assets/icons/fill/expand.png",
                         position=2,
                         selection_var=self.selection_var),
        ]

        self.frame = ctk.CTkFrame(self.root, bg_color="transparent")

        ctk.CTkLabel(master=self.frame, text=self.position).pack()

    def clicked(self):
        if not self.sidebar.collapsed:
            if self.open:
                self.up()
            else:
                self.down()
        else:
            self.selection_var.set(self.position)
            self.sidebar.change_view()


    def select(self):
        if self.sidebar.collapsed:
            print("creating classes frame")
            self.button_frame.configure(fg_color="#e97132")
            self.frame.pack(fill="both",expand=True)
            for item in self.items:
                item.deselect()

        else:
            self.down()

    def deselect(self):
        if self.sidebar.collapsed:
            print("removing classes frame")
            self.button_frame.configure(fg_color="grey")
            self.frame.pack_forget()
            for item in self.items:
                item.deselect()
        else:
            pass


    def collapse(self):
        self.button.configure(text="")
        self.up()

    def up(self):
        self.open=False
        self.button_frame.configure(fg_color="grey")
        self.menu_frame.pack_forget()
        print("up")

    def down(self):
        self.open=True
        self.button_frame.configure(fg_color="#e97132")
        self.menu_frame.pack()
        print("down")

    def expand(self):
        self.button.configure(text=self.text)
        self.frame.pack_forget()
        if self.sidebar.view.get()==self.position:
            print("was previously selected")
            self.down()
        for item in self.items:
            if item.position==self.sidebar.view.get():
                self.select()
                item.select()


        self.sidebar.set_view(self.position-1)
