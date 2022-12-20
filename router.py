from fastapi.routing import APIRouter
from api.user.views import router as user_router

api_router = APIRouter()
api_router.include_router(user_router, prefix="/user", tags=["user"])