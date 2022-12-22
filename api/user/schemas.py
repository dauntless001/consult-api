from pydantic import BaseModel, ValidationError, validator
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

class ChangePassword(BaseModel):
    current_password : str
    new_password : str
    confirm_new_password : str

    @validator('confirm_new_password')
    def passwords_match(cls, v, values, **kwargs):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('New Password & Confirm New Password Must Match')
        return v
    
    @validator("new_password")
    def password_length(cls, v, **kwargs):
        if len(v) < 8 :
            raise ValueError('Password Must be more than 8 characters')
        return v