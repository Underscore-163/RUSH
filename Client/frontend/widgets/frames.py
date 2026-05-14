import customtkinter as ctk
import PIL.Image
from frontend.widgets.styles import Fonts

class ContentFrame(ctk.CTkFrame):
    def __init__(self, master=None, title=None, icon_path=None, **kwargs):
        ctk.CTkFrame.__init__(self, master,corner_radius=13, **kwargs)
        self.fonts = Fonts()

        self.title = title
        if icon_path is not None:
            self.icon_path = icon_path
        else:
            self.icon_path = "data/app_data/static/assets/RUSH_icon.png"


        self.title_frame=ctk.CTkFrame(self)
        self.icon_label = ctk.CTkLabel(master=self.title_frame, text="", image=ctk.CTkImage(PIL.Image.open(self.icon_path)))
        self.title_label = ctk.CTkLabel(master=self.title_frame, text=self.title, font=self.fonts.get_font("extrabold",size=20))

        self.title_frame.pack(side="top", fill="x",padx=5,pady=5)
        self.icon_label.pack(side="left",padx=10,pady=5)
        self.title_label.pack(side="left",padx=5,pady=5,)

    def pack(self,**kwargs):
        ctk.CTkFrame.pack(self,padx=5,pady=5,**kwargs)

