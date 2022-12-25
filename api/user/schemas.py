from pydantic import BaseModel, ValidationError, validator, EmailStr
from uuid import UUID
from utils import validators
from datetime import datetime

class Login(BaseModel):
    email: EmailStr
    password: str

class Signup(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

    # Validators
    _validate_password = validator("password", allow_reuse=True)(validators.validate_password)

class User(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    email_verified : bool
    created_at : datetime
    updated_at : datetime

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class ChangePassword(BaseModel):
    current_password : str
    new_password : str
    confirm_new_password : str

    _validate_new_password = validator("new_password", allow_reuse=True)(validators.validate_password)

    @validator('confirm_new_password')
    def passwords_match(cls, v, values, **kwargs):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('New Password & Confirm New Password Must Match')
        return v
