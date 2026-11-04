import json
import os
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
