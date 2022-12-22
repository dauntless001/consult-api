from passlib.context import CryptContext
from fastapi import HTTPException, status

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
config_credentials = {
    'SECRET_KEY' : "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7",
    'ALGORITHM' : "HS256",
    'ACCESS_TOKEN_EXPIRE_MINUTES' : 120
}

invalid_login_credentials = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail = 'Invalid Email or Password',
    headers={"WWW-Authenticate":'Bearer'}
)

token_expired = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail = 'Invalid Authorization Token or Authorization Token Expired, Login Again',
    headers={"WWW-Authenticate":'Bearer'}
)

user_not_found = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail = 'User Not Found',
    headers={"WWW-Authenticate":'Bearer'}
)

password_not_matched = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail = 'Password Does not Match',
    headers={"WWW-Authenticate":'Bearer'}
)