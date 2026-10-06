import json
import os
import tarfile
import tempfile

def encode_assignment(assignment):
    with tarfile.TarFile(
        name=f"data/user_data/assignments/{assignment["title"]}.rush",
        mode="w",
    ) as assignment_file:

        with tempfile.NamedTemporaryFile(delete=False,mode="w") as content_file:
            content_file.write(assignment.pop("content"))
        assignment_file.add(name=content_file.name,
                            arcname="content.md")
        os.remove(content_file.name)

        attachment_names=[]
        for attachment in assignment["attachments"]:
            attachment_names.append(attachment.split("/")[-1])
            assignment_file.add(name=attachment,arcname=f"attachments/{attachment.split("/")[-1]}")
        assignment["attachments"] = attachment_names
        assignment["progress_level"]=0
        assignment["required_progress"]=5

        with tempfile.NamedTemporaryFile(delete=False,mode="w") as manifest:
            json.dump(
                assignment,
                manifest
            )
        assignment_file.add(name=manifest.name,
                            arcname="manifest.json")
        os.remove(manifest.name)

def update_manifest(assignment_path,new_values:dict):

    with tarfile.open(assignment_path,"r") as assignment_file:
        manifest = json.load(assignment_file.extractfile("manifest.json"))
    with tarfile.open(assignment_path,"a") as assignment_file:
        with tempfile.NamedTemporaryFile(delete=False, mode="w") as manifest_file:
            manifest.update(new_values)
            json.dump(
                manifest,
                manifest_file,
            )
        assignment_file.add(name=manifest_file.name,
                            arcname="manifest.json")
        os.remove(manifest_file.name)
