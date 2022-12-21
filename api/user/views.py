from fastapi import APIRouter, Depends
from api.user import schemas, services
from database import db_session
from sqlalchemy.orm import Session

router = APIRouter()
auth_handler = services.UserService()

@router.post('/login')
async def login(form:schemas.Login, session: Session = Depends(db_session)):
    userService = services.UserService(session=session)
    user = userService.login_user(form)
    return user

@router.post('/signup', response_model=schemas.User)
async def signup(form:schemas.Signup, session: Session = Depends(db_session)):
    userService = services.UserService(session=session)
    user = userService.create_user(form)
    return user

@router.post('/change-password')
async def change_password(user_id = Depends(auth_handler.auth_wrapper)):
    return user_id

