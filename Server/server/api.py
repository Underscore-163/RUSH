import asyncio
import os
from typing import Annotated

import utils
if __name__=="__main__":
    log,config=asyncio.run(utils.full_setup())
else:
    log,config=asyncio.run(utils.part_setup())

import uvicorn
from fastapi import FastAPI, UploadFile, Response, Header
import database
from body import AuthorisationHeaders, BaseTokenHeader
app = FastAPI()

@app.get("/test")
async def test(auth_headers:Annotated[AuthorisationHeaders,Header()]):

    print(auth_headers)
    authorised=await database.check_auth(token=auth_headers.token,
                                         user_id=auth_headers.user_id,
                                         client_id=auth_headers.client_id)
    if authorised==0:
        return Response(status_code=200)
    elif authorised==1:
        return Response(status_code=401)
    elif authorised==2:
        return Response(status_code=403)
    else:
        return Response(status_code=500)

@app.get("/auth")
async def auth(username,password,client_id,base_token_header:Annotated[BaseTokenHeader,Header()]):
    base_token=base_token_header.base_token
    if base_token!=config["authentication"]["base_token"]:
        return Response(status_code=403)
    
    log.info(f"auth request from {username}")
    auth_info=await database.create_auth(username=username,
                                         password=password,
                                         client_id=client_id)
    print(auth_info)
    if auth_info==1:
        return Response(status_code=401)
    elif auth_info==2:
        return Response(status_code=403)
    else:
        return auth_info



def start_server():
    log.info("Starting uvicorn")
    uvicorn.run("api:app",
                host="127.0.0.1",
                port=config["api"]["port"],
                loop="asyncio",
                ssl_certfile="config/cert.pem",
                ssl_keyfile="config/key.pem",)

if __name__ == "__main__":
    start_server()