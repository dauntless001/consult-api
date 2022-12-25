from fastapi import APIRouter, Depends, Request
from api.user import schemas, services
from database import db_session
from sqlalchemy.orm import Session
from pydantic import EmailStr
from utils.email import password_reset_mail, verification_mail
from utils.message import get_message

router = APIRouter()
auth_handler = services.UserService()

@router.post('/login')
async def login(form:schemas.Login, session: Session = Depends(db_session)):
    userService = services.UserService(session=session)
    user = userService.login_user(form)
    return user

@router.post('/signup', response_model=schemas.User)
async def signup(form:schemas.Signup, request : Request, session: Session = Depends(db_session)):
    userService = services.UserService(session=session)
    user = userService.create_user(form)
    token = userService.create_access_token({'id':f'{user.id}', 'email':user.email})
    verification_mail(request, user, token)
    data = {
        'user' : user,
        'message' : f"A verification link has been sent to {user.email}, Please Click on the link to verify"
    }
    return data

@router.post('/change-password')
async def change_password(form : schemas.ChangePassword, session: Session = Depends(db_session),user_id = Depends(auth_handler.auth_wrapper)):
    userService = services.UserService(session=session)
    change_password = userService.change_password(user_id, form)
    return change_password


@router.post('/reset-password')
async def reset_password(email : EmailStr, request : Request, session: Session = Depends(db_session)):
    userService = services.UserService(session=session)
    user = userService.get_user_by_email(email)
    token = userService.create_access_token({'id':f'{user.id}', 'email':user.email})
    return password_reset_mail(request, user, token)



@router.post('/reset-password/{token}')
async def reset_password_token(token : str,password : str, session: Session = Depends(db_session)):
    userService = services.UserService(session=session)
    payload = userService.decode_token(token)
    user = userService.get_user_by_id(payload['id'])
    user.password = password
    session.commit()
    return get_message('Password Reset Successful', 200)


@router.get('/verify-email')
async def verify_email(email : EmailStr, request: Request, session: Session = Depends(db_session)):
    userService = services.UserService(session=session)
    user = userService.get_user_by_email(email)
    token = userService.create_access_token({'id':f'{user.id}', 'email':user.email})
    return verification_mail(request, user, token)


@router.get('/verify-email/{token}')
async def verify_email_token(token : str, session : Session = Depends(db_session)):
    userService = services.UserService(session=session)
    payload = userService.decode_token(token)
    user = userService.get_user_by_id(payload['id'])
    user.email_verified = True
    session.commit()
    return get_message('Email Verification Successful', 200)
