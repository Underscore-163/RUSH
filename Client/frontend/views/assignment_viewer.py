import tempfile
import zipremove as zipfile

from Client.frontend.widgets.styles import Fonts, Colours, Icons
from Client.frontend.widgets.frames import ScrollableContentFrame, MDFrame, AttachmentsFrame
from Client.frontend.widgets.progress_tracker import ProgressTracker
from Client.backend.assignment_encoder import update_manifest, add_student_work
from Client.backend.assignment_decoder import decode_assignment
import Client.backend.utils as utils


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
                                                  write_permission=False,
                                                  height=25,
                                                  open_file_callback=self.open_compressed_attachment,
                                                  )
        self.student_work_frame = AttachmentsFrame(master=self,
                                                   title="Student Work:",
                                                   paths=self.assignment["student_work"],
                                                   height=25,
                                                   remove_file_callback=self.remove_student_work,
                                                   open_file_callback=self.open_compressed_student_work,
                                                   )

        self.attachments_frame.pack(side="top",fill="both",pady=5,padx=5,)
        self.student_work_frame.pack(side="top", fill="both", pady=5, padx=5,)

    def update_file(self):
        self.assignment["progress_level"] = self.progress_tracker.get_step()
        new_paths=[]
        for file_path in self.student_work_frame.get_paths():
            if file_path not in self.assignment["student_work"]:
                new_paths.append(file_path)
        add_student_work(self.assignment_path,new_paths)
        #update_manifest(self.assignment_path,{"progress_level":self.assignment["progress_level"]})

    def open_compressed_attachment(self,attachment_path):
        with zipfile.ZipFile(self.assignment_path) as assignment_file:
            buffer=assignment_file.open(f"attachments/{attachment_path}")
            with tempfile.NamedTemporaryFile(delete=False,suffix="."+attachment_path.split(".")[-1]) as temp_file:
                temp_file.write(buffer.read())
                utils.open_file(temp_file.name)

    def open_compressed_student_work(self,attachment_path):
        with zipfile.ZipFile(self.assignment_path) as assignment_file:
            buffer=assignment_file.open(f"student_work/{attachment_path}")
            with tempfile.NamedTemporaryFile(delete=False,suffix="."+attachment_path.split(".")[-1]) as temp_file:
                temp_file.write(buffer.read())
                utils.open_file(temp_file.name)

    def remove_student_work(self,path):
        index = self.student_work_frame.paths.index(path)
        self.student_work_frame.paths.pop(index)
        self.student_work_frame.file_widgets.pop(index)
        update_manifest(self.assignment_path,{"student_work":self.student_work_frame.get_paths()})
        with zipfile.ZipFile(self.assignment_path,mode="a") as assignment_file:
            assignment_file.remove(f"student_work/{path}")


    def pack(self,**kwargs):
        ScrollableContentFrame.pack(self,expand=True,fill="both",**kwargs)