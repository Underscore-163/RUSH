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

