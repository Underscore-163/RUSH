import customtkinter as ctk
from customtkinter import CTkImage
from Client.frontend.widgets.frames import ContentFrame
from Client.frontend.widgets.styles import Fonts, Colours, Icons
import PIL.Image

class Sidebar(ctk.CTkFrame):
    def __init__(self,master,):
        self.fonts = Fonts()
        self.colours = Colours()
        self.icons = Icons()
        ctk.CTkFrame.__init__(self,master,corner_radius=0,border_width=0,fg_color=self.colours.blue_grey)
        self.sidebar=ContentFrame(self,)
        self.sidebar.icon_label.configure(image=CTkImage(PIL.Image.open("data/app_data/static/assets/RUSH_logo.png"),size=(100,20)))

        self.collapse_button = ctk.CTkButton(self.sidebar,command=self.collapse,height=40,width=40,text="",image=CTkImage(self.icons.icon("data/app_data/static/assets/collapse.png",self.colours.white),size=(30,30)))
        self.expand_button = ctk.CTkButton(self.sidebar, command=self.expand, height=40, width=40, text="",image=CTkImage(self.icons.icon("data/app_data/static/assets/expand.png",self.colours.white), size=(30, 30)))
        self.views={}
        self.view=None
        self.collapsed=False
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=10)
        self.rowconfigure(0,weight=100)
        self.collapse_button.pack(side="bottom",padx=5,pady=5,anchor="e")

    def pack(self,**kwargs):
        ctk.CTkFrame.pack(self,side="left",fill="both",expand=True)
        self.sidebar.grid(row=0,column=0,padx=5,pady=5,sticky="nsew")

    def set_view(self,name:str):
        if self.view is not None:
            self.view.deselect()
        self.view=self.views[name]
        self.view.select()
        self.master.title(f"RUSH - {self.view.name}")

    def get_view(self):
        return self.view.name

    def get_frame(self,name:str):
        return self.views[name]

    def add_view(self,name:str,icon_path="data/app_data/static/assets/RUSH_icon-outline.png"):
        self.views[name]=SidebarView(self,name,icon_path)
        if self.view is None:
            self.set_view(name)
        return self.views[name]

    def collapse(self):
        for view in self.views.values():
            view.button.configure(text="",width=40)
            view.button.pack_forget()
            view.button.pack(padx=5,pady=5,ipadx=5,ipady=5)
        self.sidebar.icon_label.configure(image=CTkImage(PIL.Image.open("data/app_data/static/assets/RUSH_icon.png"),size=(25,25)))
        self.columnconfigure(1, weight=100)
        self.sidebar.title_label.pack_forget()
        self.collapse_button.pack_forget()
        self.expand_button.pack(side="bottom",padx=10,pady=10,anchor="w",fill="x")
        self.collapsed=True

    def expand(self):
        for view in self.views.values():
            view.button.configure(text=view.name,width=100)
            view.button.pack_forget()
            view.button.pack(padx=5,pady=5,fill="x",ipadx=5,ipady=5)
        self.sidebar.icon_label.configure(image=CTkImage(PIL.Image.open("data/app_data/static/assets/RUSH_logo.png"),size=(100,20)))
        self.columnconfigure(1, weight=10)
        self.expand_button.pack_forget()
        self.collapse_button.pack(side="bottom", padx=10, pady=10, anchor="e")
        self.collapsed=False


class SidebarView(ContentFrame):
    def __init__(self,master,name:str,icon_path="data/app_data/static/assets/RUSH_icon-outline.png"):
        ContentFrame.__init__(self,master,title=name,icon_path=icon_path)
        self.master=master
        self.name=name
        self.icon_path = icon_path
        self.fonts=Fonts()
        self.colours=Colours()
        self.icons=Icons()

        self.selected_icon=ctk.CTkImage(self.icons.icon(self.icon_path, self.colours.white), size=(30,30))
        self.deselected_icon = ctk.CTkImage(self.icons.icon(self.icon_path, self.colours.primary), size=(30, 30))


        self.button=ctk.CTkButton(self.master.sidebar,
                                  text=self.name,
                                  font=self.fonts.get_font("bold",size=17),
                                  command=self.set,
                                  fg_color=self.colours.blue_grey,
                                  height=40,
                                  image=self.deselected_icon,
                                  anchor="w")
        self.button.pack(padx=5,pady=5,fill="x",ipadx=5,ipady=5)

    def set(self):
        self.master.set_view(self.name)

    def select(self):
        self.grid(row=0, column=1, sticky="nsew", padx=5, pady=5, rowspan=2, )
        self.button.configure(fg_color=self.colours.primary,
                              image=self.selected_icon)


    def deselect(self):
        self.grid_forget()
        self.button.configure(fg_color=self.colours.blue_grey,
                              image=self.deselected_icon)

