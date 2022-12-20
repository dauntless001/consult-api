from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import db_session
from passlib.context import CryptContext
from models.user import User
from datetime import datetime, timedelta
from .schemas import Signup

pwd_crypt = CryptContext(schemes=['bcrypt'], deprecated='auto')
config_credentials = {
    'SECRET_KEY' : "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7",
    'ALGORITHM' : "HS256",
    'ACCESS_TOKEN_EXPIRE_MINUTES' : 30
}

authorized_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail = 'Invalid Email or Password',
    headers={"WWW-Authenticate":'Bearer'}
)

class UserService:
    def __init__(self, session: Session = Depends(db_session)):
        self.session = session

    async def create_user(self, user: Signup) -> User:
        password = self.get_hashed_password(user.password)
        user.password = password
        new_user = User(**user.dict())
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return new_user
    
    def get_hashed_password(self, password):
        return pwd_crypt.hash(password)