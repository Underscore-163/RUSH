import tarfile
import RUSH_exceptions as exceptions
import warnings
import json
import os

def decode_assignment(filepath):

    #check that the assignment file exists/is valid, etc.
    if not os.path.exists(filepath):
        raise FileNotFoundError("Could not locate assignment file")
    elif not os.path.isfile(filepath):
        raise IsADirectoryError
    elif not tarfile.is_tarfile(filepath):
        raise TypeError("Not an assignment file")

    #get the name of the file from the filepath, as we need it for the relative path for extraction.
    filename=(filepath.split("\\")[-1]).split(".")[0]

    #extract and decode the assignment
    with (tarfile.open(filepath) as tar):
        try:
            decoded_assignment=json.load(tar.extractfile(f"{filename}/manifest.json"))
        except Exception as e:
            # this will happen if reading of manifest.json occurs for any reason.
            # it will cause the rest of the decoding to be aborted, as it raises an error.
            raise exceptions.AssignmentReadError("Failed to locate or read manifest.json. Assignment may be corrupt.")

        try:
            decoded_assignment["content"]=tar.extractfile(f"{filename}/content.md").read()
        except:
            # this will happen if reading of content.md occurs for any reason.
            # at this point we have successfully read manifest.json, so the overall file is not corrupt
            # so it only raises a warning and replaces the content with an empty string.
            # this warning can be caught and displayed to the user.
            decoded_assignment["content"] =""
            warnings.warn("content.md was unreadable. No content is available for this assignment.",exceptions.AssignmentNoContentWarning)
        
    return decoded_assignment



print(decode_assignment(r"C:\Users\reube\OneDrive - Cognita Schools\A Level\_Computer Science\Coding\repos\RUSH\Client\data\user_data\assignments\test assignment(corrupt).rush"))