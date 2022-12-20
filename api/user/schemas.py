from pydantic import BaseModel
from uuid import UUID

class Login(BaseModel):
    email: str
    password: str

class Signup(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

class User(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: str
    password: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str