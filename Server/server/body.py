import pydantic
from fastapi import UploadFile

class Request(pydantic.BaseModel):
    auth:str

class Authentication(pydantic.BaseModel):
    username: str
    password: str
    client_id: str



