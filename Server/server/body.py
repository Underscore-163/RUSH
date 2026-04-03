import pydantic
from fastapi import UploadFile

class AuthorisationHeaders(pydantic.BaseModel):
    token:str
    user_id:str
    client_id:str

class BaseTokenHeader(pydantic.BaseModel):
    base_token:str


