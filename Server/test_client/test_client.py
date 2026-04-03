import requests
import json

def test():
    with open("user_info.json", "r") as f:
        user_info = json.load(f)
    with open("auth_info.json", "r") as f:
        auth_info = json.load(f)
    headers={"token":auth_info["Token"],
             "user_id":user_info["UserID"],
             "client_id":user_info["ClientID"]}
    params={}
    response=requests.get("http://localhost:8000/test",params=params,headers=headers)
    return response

def authorise():
    with open("user_info.json", "r") as f:
        user_info = json.load(f)
    headers={"base_token":"thisisnotthebasetoken"}
    params={
        "username":user_info["Username"],
        "password":user_info["Password"],
        "client_id":user_info["ClientID"]
    }
    response=requests.get("http://localhost:8000/auth",params=params,headers=headers)
    if response.status_code==200:
        with open("auth_info.json","w") as f:
            json.dump(response.json(),f)


authorise()