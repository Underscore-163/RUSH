import json
import os
import zipremove as zipfile
from Client.backend.assignment_decoder import get_manifest

def encode_assignment(assignment):
    with zipfile.ZipFile(
        file=f"data/user_data/assignments/{assignment["title"]}.rushzip",
        mode="w",
    ) as assignment_file:

        assignment_file.writestr("content.md",assignment.pop("content"))

        assignment_file.mkdir("student_work")

        attachment_names=[]
        for attachment in assignment["attachments"]:
            attachment_names.append(attachment.split("/")[-1])
            assignment_file.write(filename=attachment,arcname=f"attachments/{attachment.split("/")[-1]}")

        assignment["attachments"] = attachment_names
        assignment["progress_level"]=0
        assignment["required_progress"]=5

        assignment_file.writestr("manifest.json",json.dumps(assignment))


def update_manifest(assignment_path,new_values:dict):
    manifest=get_manifest(assignment_path)

    with zipfile.ZipFile(assignment_path,"a") as assignment_file:
        assignment_file.remove("manifest.json")
        manifest.update(new_values)
        assignment_file.writestr("manifest.json",json.dumps(manifest))

def add_student_work(assignment_path,new_paths:list):
    paths = get_manifest(assignment_path)["student_work"]
    with zipfile.ZipFile(assignment_path, "a") as assignment_file:
        for path in new_paths:
            paths.append(path.split("/")[-1])
            assignment_file.write(filename=path, arcname=f"student_work/{path.split("/")[-1]}")
    update_manifest(assignment_path,{"student_work":paths})

