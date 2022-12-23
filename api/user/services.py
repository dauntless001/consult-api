from fastapi import Depends, Security
from sqlalchemy.orm import Session
from database import db_session
from models.user import User
from datetime import datetime, timedelta
from .schemas import Signup, Login, ChangePassword
from utils import auth, message
from models.user import User
from sqlmodel import select
from jose import jwt
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


class UserService:
    def __init__(self, session: Session = Depends(db_session)):
        self.session = session

    def create_user(self, user: Signup) -> User:
        statement = select(User).where(User.email == user.email)
        user_exist = self.session.execute(statement).scalars().first()
        if not user_exist:
            password = self.get_hashed_password(user.password)
            user.password = password
            new_user = User(**user.dict())
            self.session.add(new_user)
            self.session.commit()
            self.session.refresh(new_user)
            return new_user
        raise message.get_message('Email Already Exist', 401)
    
    def get_hashed_password(self, password):
        return auth.password_context.hash(password)
    
    def verify_password(self, plain_password, hashed_password):
        return auth.password_context.verify(plain_password, hashed_password)
    
    def authenticate_user(self, email: str, password: str):
        statement = select(User).where(User.email == email)
        user = self.session.execute(statement).scalars().first()
        if user:
            if self.verify_password(password, user.password):
                return user
        return False
    
    def create_access_token(self, data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=auth.config_credentials['ACCESS_TOKEN_EXPIRE_MINUTES'])
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, auth.config_credentials['SECRET_KEY'], algorithm=auth.config_credentials['ALGORITHM'])
        return encoded_jwt

    def login_user(self, user : Login):
        user = self.authenticate_user(user.email, user.password)
        if not user:
            raise message.get_message('Invalid Email or Password', 401)
        access_token = self.create_access_token(
            data={"sub":f'{user.id}'}, expires_delta=timedelta(minutes=auth.config_credentials['ACCESS_TOKEN_EXPIRE_MINUTES'])
        )
        data = {"user": user, "bearer_token": f'{access_token}'}
        data['message'] = 'Login Successful'
        return data
    
    def get_user_by_id(self, id):
        statement = select(User).where(User.id == id)
        user = self.session.execute(statement).scalars().first()
        if not user:
            raise message.get_message('User Not Found', 404)
        return user
    
    def change_password(self, user_id : str, password : ChangePassword):
        user = self.get_user_by_id(user_id)
        if not self.verify_password(password.current_password, user.password):
            raise message.get_message("Password Does not Match")
        user.password = self.get_hashed_password(password.new_password)
        self.session.commit()
        return {"message" : "Password Changed Successfully", "user":user}

    
    def auth_wrapper(self, token : HTTPAuthorizationCredentials = Security(HTTPBearer())):
        try:
            payload = jwt.decode(token.credentials,auth.config_credentials['SECRET_KEY'], auth.config_credentials['ALGORITHM'])
            return payload['sub']
        except:
            raise message.get_message("Invalid Authorization Token or Authorization Token Expired, Login Again", 401)
    