import asyncio
import utils
if __name__=="__main__":
    log,config=asyncio.run(utils.full_setup())
else:
    log,config=asyncio.run(utils.part_setup())

import uvicorn
from fastapi import FastAPI, UploadFile, Response
import database
from body import Request, Authentication
app = FastAPI()


@app.get("/auth")
async def auth(username,password,client_id):
    auth_info=await database.create_auth(username=username,
                                         password=password,)
    if auth_info:
        return auth_info
    else:
        return Response(status_code=401)



async def start_server():
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    asyncio.run(start_server())