import customtkinter as ctk
from Client.frontend.widgets.styles import Fonts, Colours, Icons


class VerticalTrackerBar(ctk.CTkFrame):
    def __init__(self, master, steps:int, **kwargs):
        ctk.CTkFrame.__init__(self, master=master, border_width=0, corner_radius=0, fg_color="transparent", **kwargs)
        self.fonts = Fonts()
        self.colours = Colours()
        self.icons = Icons()

        self.steps = steps
        self.step=3

        self.in_lines=[]
        self.out_lines=[]
        self.nodes=[]

        for i in range(self.steps):
            self.in_lines.append(ctk.CTkFrame(
                master=self,
                width=10,
                height=20,
                corner_radius=0,
                fg_color=self.colours.blue_grey,
                border_color=self.colours.blue_grey,
            ))
            self.out_lines.append(ctk.CTkFrame(
                master=self,
                width=10,
                height=20,
                corner_radius=0,
                fg_color=self.colours.blue_grey,
                border_color=self.colours.blue_grey,
            ))
            self.nodes.append(ctk.CTkFrame(
                master=self,
                width=30,
                height=30,
                corner_radius=100,
                fg_color=self.colours.blue_grey,
                border_color=self.colours.blue_grey,
            ))
        for i in range(steps):
            self.in_lines[i].pack(fill="y",expand=True)
            self.nodes[i].pack()
            self.out_lines[i].pack(fill="y",expand=True)

        self.set_progress(0)

    def set_progress(self, progress):
        self.step=progress-1

        for widgets in [self.in_lines,self.out_lines,self.nodes]:
            for widget in widgets:
                widget.configure(fg_color=self.colours.blue_grey,
                              border_color=self.colours.blue_grey,)

        for i in range(0,self.step+1):
            self.in_lines[i].configure(fg_color=self.colours.primary,
                                       border_color=self.colours.primary,)
            self.nodes[i].configure(fg_color=self.colours.primary,
                                    border_color=self.colours.primary,)
            self.out_lines[i].configure(fg_color=self.colours.primary,
                                          border_color=self.colours.primary,)

    def get_progress(self):
        return self.step

    def increment_progress(self):
        self.set_progress(self.step+1)





class ProgressTracker(ctk.CTkFrame):

    def __init__(self,master,set_date,due_date,**kwargs):
        class StepFrame(ctk.CTkFrame):
            def __init__(self, master, title, **kwargs):

                self.fonts = Fonts()
                self.colours = Colours()

                ctk.CTkFrame.__init__(self, master, fg_color=self.colours.mid_grey, **kwargs)

                self.title = title
                self.title_label = ctk.CTkLabel(master=self, text=self.title,
                                                font=self.fonts.get_font("medium"),
                                                text_color=self.colours.blue_grey,
                                                height=10)
                self.title_label.pack(padx=5,pady=5, side="top", anchor="w")

        self.fonts = Fonts()
        self.colours = Colours()
        self.icons = Icons()

        self.master = master

        self.step=0
        self.set_date = set_date
        self.due_date = due_date
        self.days_remaining=3


        ctk.CTkFrame.__init__(self,master=self.master,)

        # this makes all the rows an even size.
        # uniform can be any non-empty string, as all this does is put every row
        # into the same group, making them all the same size.
        self.rowconfigure(index=list(range(6)), uniform="_", weight=1)

        self.progress_bar=VerticalTrackerBar(self,6)
        self.progress_bar.grid(row=0,column=1,sticky="nsew",padx=5,pady=1,rowspan=6,)

        self.step_frames = {
            "set": StepFrame(master=self, title="Set:",),
            "opened": StepFrame(master=self, title="Opened", border_color=self.colours.secondary),
            "in_progress": StepFrame(master=self, title="In Progress"),
            "done": StepFrame(master=self, title="Done"),
            "handed_in": StepFrame(master=self, title="Handed in"),
            "due": StepFrame(master=self, title="Due:"),
        }

        for i in range(len(self.step_frames.values())):
            list(self.step_frames.values())[i].grid(row=i, column=0, sticky="nsew", padx=5, pady=5,)

        self.set_date_label=ctk.CTkLabel(master=self.step_frames["set"],
                                         text=self.set_date,
                                         font=self.fonts.get_font("bold",size=15),
                                         height=10
                                         )
        self.set_date_label.pack(padx=5,pady=5,side="bottom",anchor="w")

        self.mark_in_progress_button=ctk.CTkButton(master=self.step_frames["opened"],
                                                   text="Mark as 'In Progress'",
                                                   image=ctk.CTkImage(self.icons.icon("data/app_data/static/assets/tick.png",self.colours.mid_grey),size=(15,15)),
                                                   font=self.fonts.get_font("bold",size=15),
                                                   text_color=self.colours.mid_grey,
                                                   anchor="w",
                                                   command=self.mark_in_progress
                                                   )
        self.mark_in_progress_button.pack(padx=5, pady=5, side="bottom", anchor="w",fill="x")

        self.mark_done_button = ctk.CTkButton(master=self.step_frames["in_progress"],
                                                     text="Mark as 'Done'",
                                                     image=ctk.CTkImage(
                                                         self.icons.icon("data/app_data/static/assets/tick.png",
                                                                         self.colours.mid_grey), size=(15, 15)),
                                                     font=self.fonts.get_font("bold", size=10),
                                                     text_color=self.colours.mid_grey,
                                                     anchor="w",
                                                     state="disabled",
                                                     command=self.mark_done,
                                                     fg_color=self.colours.dark_grey
                                                     )
        self.mark_done_button.pack(padx=5, pady=5, side="left", anchor="s",)

        self.add_work_button = ctk.CTkButton(master=self.step_frames["in_progress"],
                                                     text="Add Work",
                                                     image=ctk.CTkImage(
                                                         self.icons.icon("data/app_data/static/assets/plus.png",
                                                                         self.colours.mid_grey), size=(15, 15)),
                                                     font=self.fonts.get_font("bold", size=10),
                                                     text_color=self.colours.mid_grey,
                                                     anchor="w",
                                                     state="disabled",
                                                     fg_color=self.colours.dark_grey
                                                     )
        self.add_work_button.pack(padx=5, pady=5, side="right", anchor="s",)

        self.hand_in_button = ctk.CTkButton(master=self.step_frames["done"],
                                                     text="Hand In",
                                                     image=ctk.CTkImage(
                                                         self.icons.icon("data/app_data/static/assets/hand_in.png",
                                                                         self.colours.mid_grey), size=(15, 15)),
                                                     font=self.fonts.get_font("bold", size=15),
                                                     text_color=self.colours.mid_grey,
                                                     fg_color=self.colours.dark_grey,
                                                     anchor="w",
                                                     state="disabled",
                                                     command=self.hand_in
                                                     )
        self.hand_in_button.pack(padx=5, pady=5, side="bottom", anchor="w",fill="x")

        self.days_remaining_label = ctk.CTkLabel(master=self.step_frames["due"],
                                                 text=f"{self.days_remaining} days remaining",
                                                 font=self.fonts.get_font("medium", size=15),
                                                 text_color=self.colours.primary,
                                                 height=10)
        self.days_remaining_label.pack(padx=5, pady=5, side="bottom", anchor="w")

        self.due_date_label = ctk.CTkLabel(master=self.step_frames["due"],
                                           text=self.due_date,
                                           font=self.fonts.get_font("bold", size=15),
                                           height=5
                                           )
        self.due_date_label.pack(padx=5, side="bottom", anchor="w")

        self.progress_bar.set_progress(2)

    def mark_in_progress(self):
        self.step=3
        self.progress_bar.set_progress(self.step)

        self.step_frames["opened"].configure(border_color=self.colours.dark_grey)
        self.step_frames["in_progress"].configure(border_color=self.colours.secondary)

        self.mark_in_progress_button.configure(state="disabled",
                                               fg_color=self.colours.dark_grey,
                                               image=ctk.CTkImage(
                                                   self.icons.icon("data/app_data/static/assets/tick.png",
                                                                   self.colours.blue_grey),
                                                   size=(15,15)),)

        self.add_work_button.configure(state="normal",
                                               fg_color=self.colours.primary,
                                               image=ctk.CTkImage(
                                                   self.icons.icon("data/app_data/static/assets/plus.png",
                                                                   self.colours.white),
                                                   size=(15, 15)),
                                               text_color=self.colours.white,)

        self.mark_done_button.configure(state="normal",
                                       fg_color=self.colours.primary,
                                       image=ctk.CTkImage(
                                           self.icons.icon("data/app_data/static/assets/tick.png",
                                                           self.colours.white),
                                           size=(15, 15)),
                                       text_color=self.colours.white,)


    def mark_done(self):
        self.step = 4
        self.progress_bar.set_progress(self.step)

        self.step_frames["in_progress"].configure(border_color=self.colours.dark_grey)
        self.step_frames["done"].configure(border_color=self.colours.secondary)

        self.mark_done_button.configure(state="disabled",
                                               fg_color=self.colours.dark_grey,
                                               image=ctk.CTkImage(
                                                   self.icons.icon("data/app_data/static/assets/tick.png",
                                                                   self.colours.blue_grey),
                                                   size=(15, 15)), )
        self.add_work_button.configure(state="disabled",
                                        fg_color=self.colours.dark_grey,
                                        image=ctk.CTkImage(
                                            self.icons.icon("data/app_data/static/assets/plus.png",
                                                            self.colours.blue_grey),
                                            size=(15, 15)), )


        self.hand_in_button.configure(state="normal",
                                        fg_color=self.colours.primary,
                                        image=ctk.CTkImage(
                                            self.icons.icon("data/app_data/static/assets/tick.png",
                                                            self.colours.white),
                                            size=(15, 15)),
                                        text_color=self.colours.white, )

    def hand_in(self):
        self.step = 5
        self.progress_bar.set_progress(self.step)

        self.step_frames["done"].configure(border_color=self.colours.dark_grey)
        self.step_frames["handed_in"].configure(border_color=self.colours.secondary)

        self.hand_in_button.configure(state="disabled",
                                        fg_color=self.colours.dark_grey,
                                        image=ctk.CTkImage(
                                            self.icons.icon("data/app_data/static/assets/hand_in.png",
                                                            self.colours.blue_grey),
                                            size=(15, 15)), )

