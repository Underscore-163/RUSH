import datetime
import tarfile
import tkinter as tk
import customtkinter as ctk
import tkcalendar
from Client.frontend.widgets.combobutton import ComboButton
from Client.frontend.widgets.styles import Fonts, Colours, Icons
from Client.frontend.widgets.frames import MDFrame, AttachmentsFrame
from Client.backend.assignment_encoder import encode_assignment

class AssignmentEditor(ctk.CTkScrollableFrame):
    def __init__(self,master,**kwargs):
        self.fonts=Fonts()
        self.colours=Colours()
        self.icons=Icons()
        ctk.CTkScrollableFrame.__init__(self,master=master,**kwargs)

        for i in range(2):
            self.columnconfigure(i,weight=1)
        self.columnconfigure(2,weight=1)
        self.rowconfigure(0,weight=5)
        self.rowconfigure(1, weight=0)


        self.name_input=ctk.CTkEntry(master=self,height=30,placeholder_text="Assignment Name")
        self.content_input=ctk.CTkTextbox(master=self,
                                          border_color=self.colours.dark_grey,
                                          border_width=1,
                                          corner_radius=10,)
        self.content_preview=MDFrame(master=self,width=30)

        self.settings_frame=ctk.CTkFrame(master=self,)

        self.set_date_label=ctk.CTkLabel(master=self.settings_frame,
                                         text="Set Date:",
                                         font=self.fonts.get_font("bold",15),)
        self.set_date_picker=tkcalendar.DateEntry(master=self.settings_frame,
                                                  font=self.fonts.get_font("medium",20,),
                                                  mindate=datetime.date.today(),
                                                  locale="en_GB",
                                                  background=self.colours.secondary,
                                                  headersbackground=self.colours.tertiary,
                                                  headersforeground=self.colours.white,
                                                  selectbackground=self.colours.primary,
                                                  weekendbackground=self.colours.light_grey,
                                                  weekendforeground=self.colours.black,
                                                  disableddaybackground=self.colours.dark_grey,
                                                  showweeknumbers=False
                                                  )
        self.assignee_label=ctk.CTkLabel(master=self.settings_frame,
                                         text="Assignees:",
                                         font=self.fonts.get_font("bold",15),)
        self.assignee_dropdown=ctk.CTkComboBox(master=self.settings_frame,values=["10f649612a6f3741a6907e1561bcc430f8"])
        self.due_date_label=ctk.CTkLabel(master=self.settings_frame,
                                         text="Due Date:",
                                         font=self.fonts.get_font("bold",15),)
        self.due_date_picker=tkcalendar.DateEntry(master=self.settings_frame,
                                                  font=self.fonts.get_font("medium",20,),
                                                  mindate=datetime.date.today(),
                                                  locale="en_GB",
                                                  background=self.colours.secondary,
                                                  headersbackground=self.colours.tertiary,
                                                  headersforeground=self.colours.white,
                                                  selectbackground=self.colours.primary,
                                                  weekendbackground=self.colours.light_grey,
                                                  weekendforeground=self.colours.black,
                                                  disableddaybackground=self.colours.dark_grey,
                                                  showweeknumbers=False
                                                  )
        self.assign_button=ComboButton(master=self.settings_frame,
                                       title="Done",
                                       commands={
                                           "Assign Now":lambda: encode_assignment(self.get_assignment_data()),
                                           "Save":lambda: encode_assignment(self.get_assignment_data())
                                       })

        self.set_date_label.pack(pady=5,padx=10,anchor="nw")
        self.set_date_picker.pack(padx=10,anchor="nw")
        self.assignee_label.pack(pady=5,padx=10,anchor="nw")
        self.assignee_dropdown.pack(pady=5,padx=10,anchor="nw",fill="x")
        self.due_date_label.pack(pady=5,padx=10,anchor="nw")
        self.due_date_picker.pack(padx=10,anchor="nw",)
        self.assign_button.pack(pady=5,padx=10,anchor="nw",side="bottom")



        self.name_input.grid(column=0,row=0,sticky="nsew",columnspan=2,pady=5,padx=5)
        self.content_input.grid(column=0,row=1,sticky="nsew",padx=5)
        self.content_preview.grid(column=1,row=1,sticky="nsew",padx=5)
        self.settings_frame.grid(column=2,row=1,sticky="nsew",rowspan=2,pady=5,padx=5)

        ctk.CTkLabel(self,
                     text="Preview (may not be accurate)",
                     font=self.fonts.get_font("medium",10,True),
                     text_color=self.colours.dark_grey,
                     bg_color=self.colours.light_grey).grid(column=1,row=1,sticky="se",padx=10,pady=5)

        self.content_input.bind("<Key>",self.update_preview)

        self.attachments_frame=AttachmentsFrame(master=self)
        self.attachments_frame.grid(column=0,row=2,columnspan=2,sticky="nsew",pady=5,padx=5)



    def update_preview(self,event):
        if event.keycode==8:
            self.content_preview.update_md(self.content_input.get("1.0",tk.END)[:-2])
        else:
            self.content_preview.update_md(self.content_input.get("1.0",tk.END)[:-1]+event.char)

    
    def assign(self,assignment):
        pass
    def save(self,assignment):
        pass

    def get_assignment_data(self):
        return {
            "title":self.name_input.get(),
            "date_assigned":self.set_date_picker.get_date().toordinal(),
            "date_due":self.due_date_picker.get_date().toordinal(),
            "assignees":[self.assignee_dropdown.get()],
            "content":self.content_input.get("1.0",tk.END),
            "attachments":[path for path in self.attachments_frame.get_paths()],
            "student_work":[]
        }


