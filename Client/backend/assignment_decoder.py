import zipremove as zipfile
import Client.backend.RUSH_exceptions as exceptions
import warnings
import json
import os

def decode_assignment(filepath):

    #check that the assignment file exists/is valid, etc.
    if not os.path.exists(filepath):
        raise FileNotFoundError("Could not locate assignment file")
    elif not os.path.isfile(filepath):
        raise IsADirectoryError
    elif not zipfile.is_zipfile(filepath):
        raise TypeError("Not an assignment file")

    #extract and decode the assignment
    with zipfile.ZipFile(filepath) as assignment_file:
        try:
            decoded_assignment=json.load(assignment_file.open("manifest.json"))
        except Exception as e:
            # this will happen if reading of manifest.json occurs for any reason.
            # it will cause the rest of the decoding to be aborted, as it raises an error.
            raise exceptions.AssignmentReadError("Failed to locate or read manifest.json. Assignment may be corrupt.")

        try:
            # this is a one line decoder.
            # first we extract content.md, which we read as bytes from an IO buffer
            # we then decode those bytes into UTF-8
            # next we use .replace to strip out escape characters
            # finally we use another .replace to remove the extra blank lines that inexplicably get inserted by the decoding
            decoded_assignment["content"]=assignment_file.open("content.md").read().decode("utf-8").replace("\\", "").replace("\r\n\r\n", "\r\n")

        except Exception as e:
            print(e)
            # this will happen if reading of content.md occurs for any reason.
            # at this point we have successfully read manifest.json, so the overall file is not corrupt
            # so it only raises a warning and replaces the content with an empty string.
            # this warning can be caught and displayed to the user.
            decoded_assignment["content"] =""
            warnings.warn("content.md was unreadable. No content is available for this assignment.",exceptions.AssignmentNoContentWarning)

    return decoded_assignment

def get_manifest(assignment_path):
    with zipfile.ZipFile(assignment_path,"r") as assignment_file:
        manifest= json.loads(assignment_file.open("manifest.json").read())
        return manifest