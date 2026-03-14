import os
if __name__ == '__main__':
    os.chdir(os.getcwd().replace("server", ""))

import asyncio
import uvicorn
from fastapi import FastAPI, UploadFile, Response
import database
from body import Request, Authentication
app = FastAPI()


@app.get("/auth/{user_id}")
async def auth(user_id,username,password,client_id):

    return user_id, username, password, client_id



async def start_server():
    await uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    asyncio.run(start_server())