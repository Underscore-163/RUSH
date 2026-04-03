import pydantic
from fastapi import UploadFile

class Test(pydantic.BaseModel):
    words:str

class Query(pydantic.BaseModel):
    pass

class AuthorisationHeaders(pydantic.BaseModel):
    token:str
    user_id:str
    client_id:str



