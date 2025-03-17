from fastapi import APIRouter
from app.api.routes import users, auth, districts, user_requests

api_router = APIRouter()
api_router.include_router(users.router)
api_router.include_router(auth.router)
api_router.include_router(districts.router)
api_router.include_router(user_requests.router)
