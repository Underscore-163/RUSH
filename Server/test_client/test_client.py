import requests


def auth():
    params={
        "username":"reuben",
        "password":"reuben",
        "client_id":"12345"
    }
    response=requests.get(f"http://localhost:8000/auth",params=params)
    if response.status_code==200:
        print(response.json())
    else:
        print(response.status_code)

if __name__ == "__main__":
    auth()