import customtkinter as ctk
from customtkinter import CTkImage
from frontend.widgets.frames import ContentFrame
from frontend.widgets.styles import Fonts, Colours
import PIL.Image

class Sidebar(ctk.CTkFrame):
    def __init__(self,master,):
        ctk.CTkFrame.__init__(self,master,corner_radius=0,border_width=0,fg_color="#ebebeb")
        self.sidebar=ContentFrame(self,)
        self.sidebar.icon_label.configure(image=CTkImage(PIL.Image.open("data/app_data/static/assets/RUSH_logo.png"),size=(100,20)))
        self.fonts = Fonts()
        self.colours = Colours()
        self.views={}
        self.view=None
        self.collapsed=False
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=10)
        self.rowconfigure(0,weight=100)

    def pack(self,**kwargs):
        ctk.CTkFrame.pack(self,side="left",fill="both",expand=True)
        self.sidebar.grid(row=0,column=0,padx=5,pady=5,sticky="nsew")

    def set_view(self,name:str):
        if self.view is not None:
            self.view.grid_forget()
            self.view.button.configure(fg_color=self.colours.dark_grey)
        self.view=self.views[name]
        self.view.grid(row=0,column=1,sticky="nsew",padx=5,pady=5,rowspan=2,)
        self.view.button.configure(fg_color=self.colours.primary)
        self.master.title(f"RUSH - {self.view.name}")

    def get_view(self):
        return self.view.name

    def get_frame(self,name:str):
        return self.views[name]

    def add_view(self,name:str,icon_path=None):
        self.views[name]=SidebarView(self,name,icon_path)
        if self.view is None:
            self.set_view(name)
        return self.views[name]

    def collapse(self):
        for view in self.views.values():
            view.button.configure(text="",width=1)
        self.sidebar.icon_label.configure(image=CTkImage(PIL.Image.open("data/app_data/static/assets/RUSH_icon.png"),size=(25,25)))
        self.columnconfigure(1, weight=100)
        self.collapsed=True

    def expand(self):
        for view in self.views.values():
            view.button.configure(text=view.name,width=100)
        self.sidebar.icon_label.configure(image=CTkImage(PIL.Image.open("data/app_data/static/assets/RUSH_logo.png"),size=(100,20)))
        self.columnconfigure(1, weight=5)
        self.collapsed=False


class SidebarView(ContentFrame):
    def __init__(self,master,name:str,icon_path=None):
        ContentFrame.__init__(self,master,title=name)
        self.master=master
        self.name=name
        if icon_path is not None:
            self.icon_path = icon_path
        else:
            self.icon_path = "data/app_data/static/assets/RUSH_icon.png"
        self.fonts=Fonts()
        self.colours=Colours()

        self.button=ctk.CTkButton(self.master.sidebar,
                                  text=self.name,
                                  font=self.fonts.get_font("bold",),
                                  command=self.select,
                                  fg_color=self.colours.dark_grey,
                                  height=40,
                                  image=CTkImage(PIL.Image.open(self.icon_path),size=(18,20)),
                                  anchor="w")
        self.button.pack(padx=5,pady=5,fill="x",ipadx=5,ipady=5)

    def select(self):
        self.master.set_view(self.name)

