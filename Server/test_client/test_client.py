import requests


def auth():
    user_id=1234
    params={
        "username":"reuben@dearden.org.uk",
        "password":"12345",
        "client_id":"12345"
    }
    response=requests.get(f"http://localhost:8000/auth/{user_id}",params=params)
    print(response.json())

if __name__ == "__main__":
    auth()