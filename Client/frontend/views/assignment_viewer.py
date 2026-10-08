import tarfile

import customtkinter as ctk
from Client.frontend.widgets.styles import Fonts, Colours, Icons
from Client.frontend.widgets.frames import ScrollableContentFrame, MDFrame, AttachmentsFrame
from Client.frontend.widgets.progress_tracker import ProgressTracker
from Client.frontend.widgets.file_widget import FileWidget
from Client.backend.assignment_encoder import update_manifest, add_student_work
from Client.backend.assignment_decoder import decode_assignment


class AssignmentViewer(ScrollableContentFrame):
    def __init__(self,master,assignment_path):

        self.fonts = Fonts()
        self.colours = Colours()
        self.icons = Icons()

        self.master = master
        self.assignment = decode_assignment(assignment_path)
        self.assignment_path = assignment_path

        ScrollableContentFrame.__init__(self,self.master,title=self.assignment["title"])



        self.progress_tracker = ProgressTracker(master=self,
                                                set_date=self.assignment["date_assigned"],
                                                due_date=self.assignment["date_due"],
                                                step=self.assignment["progress_level"],)
        self.progress_tracker.pack(side="right",fill="y",padx=5,pady=5)



        self.md_frame = MDFrame(master=self,md=self.assignment["content"])
        self.md_frame.pack(side="top",fill="both",pady=5,padx=5,expand=True)



        self.attachments_frame = AttachmentsFrame(master=self,
                                                  paths=self.assignment["attachments"],
                                                  add_files_permission=False,
                                                  height=25
                                                  )
        self.student_work_frame = AttachmentsFrame(master=self,
                                                   title="Student Work:",
                                                   paths=self.assignment["student_work"],
                                                   height=25
                                                   )

        self.attachments_frame.pack(side="top",fill="both",pady=5,padx=5,)
        self.student_work_frame.pack(side="top", fill="both", pady=5, padx=5,)

    def update_file(self):
        self.assignment["progress_level"] = self.progress_tracker.get_step()
        new_paths=[]
        print(self.assignment["student_work"] is self.student_work_frame.get_paths())
        for file_path in self.student_work_frame.get_paths():
            if file_path not in self.assignment["student_work"]:
                print(file_path,"is not in the assignment")
                new_paths.append(file_path)
            else:
                print(file_path,"is already in the assignment")


        add_student_work(self.assignment_path,new_paths)
        update_manifest(self.assignment_path,{"progress_level":self.assignment["progress_level"]})



    def pack(self,**kwargs):
        ScrollableContentFrame.pack(self,expand=True,fill="both",**kwargs)