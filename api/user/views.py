from fastapi import APIRouter, Depends
from api.user import schemas, services
from database import db_session
from sqlalchemy.orm import Session

router = APIRouter()

@router.post('/login')
async def login(form:schemas.Login, session: Session = Depends(db_session)):
    userService = services.UserService(session=session)
    return {}


@router.post('/signup', response_model=schemas.User)
async def signup(form:schemas.Signup, session: Session = Depends(db_session)):
    userService = services.UserService(session=session)
    user = await userService.create_user(form)
    return user

