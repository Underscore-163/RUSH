import customtkinter as ctk
from frontend.widgets.fonts import Fonts

class ComboButton(ctk.CTkFrame):
    def __init__(self,master,commands:dict):
        ctk.CTkFrame.__init__(self,master=master,width=175,height=35,fg_color="#f07433")
        self.fonts = Fonts()

        self.commands = commands

        self.option_menu=ctk.CTkOptionMenu(self,values=list(self.commands.keys()),command=self.update_text,bg_color="#f07434")
        self.trigger_button = ctk.CTkButton(self, text=self.option_menu.get(), command=self.trigger,bg_color="#f07433",font=self.fonts.regular)

        self.option_menu.place(x=31,y=3)
        self.trigger_button.place(x=3,y=3)
        self.trigger_button.lift()

    def trigger(self):
        self.commands[self.option_menu.get()]()
    def update_text(self,*args):
        self.trigger_button.configure(text=self.option_menu.get())

