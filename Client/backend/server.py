import json
import os
import tempfile
import zipfile

import requests

def get_connection_info():
    with open("data/app_data/dynamic/connection/provision.json","r") as f:
        connection_info = json.load(f)
    with open("data/app_data/dynamic/connection/client_id","r") as f:
        connection_info["client_id"]=f.read()
    if os.path.exists("data/app_data/dynamic/connection/token"):
        with open("data/app_data/dynamic/connection/token","r") as f:
            connection_info["token"]=json.load(f)
    return connection_info


def authenticate(username,password):
    connection_info = get_connection_info()
    headers={"base_token":connection_info["base_token"]}
    params={
        "username":username,
        "password":password,
        "client_id":connection_info["client_id"],
    }
    response=requests.get(f"https://{connection_info["address"]}/auth",
                          params=params,
                          headers=headers,
                          verify=f"data/app_data/dynamic/connection/{connection_info["certificate"]}")
    if response.status_code == 200:
        with open("data/app_data/dynamic/connection/token","w") as f:
            json.dump(response.json(),f)
    return response.status_code

def test_connection():
    connection_info = get_connection_info()
    headers = {"token": connection_info["token"]["Token"],
               "user_id": connection_info["token"]["UserID"],
               "client_id": connection_info["token"]["ClientID"],}
    params = {}
    response = requests.get("https://localhost:8000/test",
                            params=params,
                            headers=headers,
                            verify=f"data/app_data/dynamic/connection/{connection_info["certificate"]}")
    print(response)

def get_assignment_list():
    connection_info = get_connection_info()
    headers = {"token": connection_info["token"]["Token"],
               "user_id": connection_info["token"]["UserID"],
               "client_id": connection_info["token"]["ClientID"], }

    response = requests.get(f"https://{connection_info["address"]}/assignments/list",
                            headers=headers,
                            verify=f"data/app_data/dynamic/connection/{connection_info["certificate"]}")
    return response


def get_assignment(assignment_id):
    connection_info = get_connection_info()
    headers = {"token": connection_info["token"]["Token"],
               "user_id": connection_info["token"]["UserID"],
               "client_id": connection_info["token"]["ClientID"], }
    params = {"assignment_id": assignment_id}
    response = requests.get(f"https://{connection_info["address"]}/assignments",
                            params=params,
                            headers=headers,
                            verify=f"data/app_data/dynamic/connection/{connection_info["certificate"]}")
    if response.status_code == 200:
        # write the file response to a non deleting tempfile
        with tempfile.NamedTemporaryFile(delete=False,mode="wb") as temp:
            temp.write(response.content)
        # open the tempfile with zip to get the title from the manifest
        with zipfile.ZipFile(temp.name) as temp_zip:
            manifest = json.loads(temp_zip.read("manifest.json"))
        # open the tempfile as bytes
        with open(temp.name,"rb") as temp_r:
            # write the bytes into the propper file
            with open(f"data/user_data/assignments/{manifest["title"]}.rushzip", "wb") as file:
                file.write(temp_r.read())
        os.remove(temp.name) # clean up the tempfile
    return response.status_code

def send_assignment(file_name):
    connection_info = get_connection_info()
    headers = {"token": connection_info["token"]["Token"],
               "user_id": connection_info["token"]["UserID"],
               "client_id": connection_info["token"]["ClientID"], }
    files={"files":open(f"data/app_data/dynamic/sync_cache/assignments/{file_name}","rb")}
    params = {"files":files}
    response = requests.post(f"https://{connection_info["address"]}/assignments",
                            params=params,
                            headers=headers,
                            files=files,
                            verify=f"data/app_data/dynamic/connection/{connection_info["certificate"]}")
    return response.status_code