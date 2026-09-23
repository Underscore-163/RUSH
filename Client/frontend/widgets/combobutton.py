import customtkinter as ctk
from Client.frontend.widgets.styles import Fonts

class ComboButtonOld(ctk.CTkFrame):
    def __init__(self,master,commands:dict):
        ctk.CTkFrame.__init__(self,master=master,width=175,height=35,fg_color="#f07433")
        self.fonts = Fonts()

        self.commands = commands

        self.option_menu=ctk.CTkOptionMenu(self,values=list(self.commands.keys()),command=self.trigger,bg_color="#f07434",)
        #self.trigger_button = ctk.CTkButton(self, text=self.option_menu.get(), command=self.trigger,bg_color="#f07433",font=self.fonts.regular)
        #self.option_menu.bind("<Button-1>",self.trigger)
        self.option_menu.place(x=31,y=3)
        #self.trigger_button.place(x=3,y=3)
        #self.trigger_button.lift()

    def trigger(self,*args):
        self.commands[self.option_menu.get()]()
    def update_text(self,*args):
        self.trigger_button.configure(text=self.option_menu.get())

class ComboButton(ctk.CTkOptionMenu):
    def __init__(self,master,title="Menu",commands:dict={},**kwargs):

        self.fonts = Fonts()

        self.master = master
        self.title = title
        self.commands = commands
        ctk.CTkOptionMenu.__init__(self,
                                   master=self.master,
                                   values=[self.title,*list(self.commands.keys())],
                                   command=self.trigger,
                                   font=self.fonts.get_font("Medium",),
                                   dropdown_font=self.fonts.get_font("Medium",),
                                   **kwargs
                                   )

    def trigger(self,*args):
        if self.get() in self.commands:
            self.commands[self.get()]()
        self.set(self.title)
