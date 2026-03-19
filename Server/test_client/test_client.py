import requests
import json

def test():
    with open("user_info.json", "r") as f:
        user_info = json.load(f)
    with open("auth_info.json", "r") as f:
        auth_info = json.load(f)
    params={
        "auth_token":auth_info["Token"],
        "user_id":user_info["UserID"],
        "client_id":user_info["ClientID"]
    }
    response=requests.get("http://localhost:8000/test",params=params)
    return response

def authorise():
    params={
        "username":user_info["Username"],
        "password":user_info["Password"],
        "client_id":user_info["ClientID"]
    }
    response=requests.get("http://localhost:8000/auth",params=params)
    with open("auth_info.json","w") as f:
        json.dump(response.json(),f)
    with open("user_info.json","w") as f:
        user_info["UserID"]=response.json()["UserID"]
        json.dump(user_info,f)

with open("user_info.json","r") as f:
    user_info=json.load(f)
with open("auth_info.json","r") as f:
    auth_info=json.load(f)


fails=0
for i in range(1):
    test_response=test()
    print(test_response)
    if test_response.status_code == 401:
        fails+=1
        print(fails)
        authorise()

print(f"{fails} tests failed")