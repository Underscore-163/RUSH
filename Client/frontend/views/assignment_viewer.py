import customtkinter as ctk
from Client.frontend.widgets.styles import Fonts, Colours, Icons
from Client.frontend.widgets.frames import ScrollableContentFrame, MDFrame
from Client.frontend.widgets.progress_tracker import ProgressTracker
from Client.frontend.widgets.file_widget import FileWidget


class AssignmentViewer(ScrollableContentFrame):
    def __init__(self,master,assignment):

        self.fonts = Fonts()
        self.colours = Colours()
        self.icons = Icons()

        self.master = master
        self.assignment = assignment

        ScrollableContentFrame.__init__(self,self.master,title=self.assignment["title"])



        self.progress_tracker = ProgressTracker(master=self,
                                                set_date=self.assignment["date_assigned"],
                                                due_date=self.assignment["date_due"],)
        self.progress_tracker.pack(side="right",fill="y",padx=5,pady=5)



        self.md_frame = MDFrame(master=self,md=self.assignment["content"])
        self.md_frame.pack(side="top",fill="both",pady=5,padx=5,expand=True)



        self.file_frame = ctk.CTkFrame(master=self)

        ctk.CTkLabel(master=self.file_frame,
                     text="Attachments:",
                     font=self.fonts.get_font("medium"),
                     text_color=self.colours.blue_grey,
                     height=10
                     ).pack(side="top",padx=10,pady=5,anchor="w")

        for file in self.assignment["attachments"]:
            FileWidget(master=self.file_frame,filepath=file).pack(fill="x",padx=5,pady=5,)

        ctk.CTkLabel(master=self.file_frame,
                     text="Your Work:",font=self.fonts.get_font("medium"),
                     text_color=self.colours.blue_grey,
                     height=10
                     ).pack(side="top",padx=10,anchor="w")

        for file in self.assignment["student_work"]:
            FileWidget(master=self.file_frame,filepath=file).pack(fill="x",padx=5,pady=5)

        ctk.CTkButton(master=self.file_frame,
                      height=35,
                      anchor="w",
                      text="Add Work",
                      font=self.fonts.get_font("bold"),
                      image=ctk.CTkImage(self.icons.icon("data/app_data/static/assets/plus.png",self.colours.white))
                      ).pack(side="top",padx=5,pady=5,anchor="w")

        self.file_frame.pack(side="top",fill="both",pady=5,padx=5,expand=True)


    def pack(self,**kwargs):
        ScrollableContentFrame.pack(self,expand=True,fill="both",**kwargs)