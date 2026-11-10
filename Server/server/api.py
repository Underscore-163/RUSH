import asyncio
import json
import os
from typing import Annotated

import utils
if __name__=="__main__":
    log,config=asyncio.run(utils.full_setup())
else:
    log,config=asyncio.run(utils.part_setup())

import uvicorn
from fastapi import FastAPI, UploadFile, Response, Header
from fastapi.responses import FileResponse
import database
from body import AuthorisationHeaders, BaseTokenHeader
app = FastAPI()


@app.get("/auth")
async def reauth(username, password, client_id, base_token_header:Annotated[BaseTokenHeader,Header()]):
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

@app.get("/assignments/list")
async def send_assignment_list(auth_headers:Annotated[AuthorisationHeaders,Header()]):
    authorised = await database.check_auth(token=auth_headers.token,
                                           user_id=auth_headers.user_id,
                                           client_id=auth_headers.client_id)
    if authorised == 0:
        assignment_ids= await database.list_assignments(auth_headers.user_id)
        return Response(status_code=200, content=json.dumps(assignment_ids))
    elif authorised == 1:
        return Response(status_code=401)
    elif authorised == 2:
        return Response(status_code=403)
    else:
        return Response(status_code=500)

@app.get("/assignments",response_class=FileResponse)
async def send_assignment(assignment_id,auth_headers:Annotated[AuthorisationHeaders,Header()]):
    authorised = await database.check_auth(token=auth_headers.token,
                                           user_id=auth_headers.user_id,
                                           client_id=auth_headers.client_id)
    if authorised == 0:
        if database.check_assigned(assignment_id,auth_headers.user_id):
            return f"data/files/assignments/{assignment_id}.rushzip"
        else:
            return Response(status_code=403)
    elif authorised == 1:
        return Response(status_code=401)
    elif authorised == 2:
        return Response(status_code=403)
    else:
        return Response(status_code=500)

@app.post("/assignments")
async def receive_assignment(files:UploadFile,auth_headers:Annotated[AuthorisationHeaders,Header()]):
    authorised = await database.check_auth(token=auth_headers.token,
                                           user_id=auth_headers.user_id,
                                           client_id=auth_headers.client_id)
    if authorised == 0:
        await database.add_assignment(assignment=files.file,creator_id=auth_headers.user_id,)
        return Response(status_code=200)
    elif authorised == 1:
        return Response(status_code=401)
    elif authorised == 2:
        return Response(status_code=403)
    else:
        return Response(status_code=500)


def start_server():
    log.info("Starting uvicorn")
    uvicorn.run("api:app",
                host=config["api"]["address"],
                port=config["api"]["port"],
                loop="asyncio",
                ssl_certfile="config/cert.pem",
                ssl_keyfile="config/key.pem",)

if __name__ == "__main__":
    start_server()