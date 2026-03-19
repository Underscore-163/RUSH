import pydantic
from fastapi import UploadFile

class Test(pydantic.BaseModel):
    words:str

class Query(pydantic.BaseModel):
    pass

class Authorisation(pydantic.BaseModel):
    auth_token:str
    user_id:str
    client_id:str



