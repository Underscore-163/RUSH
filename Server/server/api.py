import asyncio
import os

import utils
if __name__=="__main__":
    log,config=asyncio.run(utils.full_setup())
else:
    log,config=asyncio.run(utils.part_setup())

import uvicorn
from fastapi import FastAPI, UploadFile, Response
import database
from body import Authorisation, Test
app = FastAPI()

@app.get("/test")
async def test(auth_token:str,user_id:str,client_id:str):
    authorised=await database.check_auth(token=auth_token,user_id=user_id,client_id=client_id)
    if not authorised:
        return Response(status_code=401)
    else:
        return Response(status_code=200)

@app.get("/auth")
async def auth(username,password,client_id):
    log.info(f"auth request from {username}")
    auth_info=await database.create_auth(username=username,
                                         password=password,
                                         client_id=client_id)
    if auth_info is True:
        return auth_info
    elif auth_info is False:
        return Response(status_code=401)
    elif auth_info is None:
        return Response(status_code=None)



def start_server():
    log.info("Starting uvicorn")
    uvicorn.run("api:app", host="127.0.0.1", port=config["api"]["port"],loop="asyncio")

if __name__ == "__main__":
    start_server()