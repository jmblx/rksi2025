from dishka.integrations.fastapi import (
    DishkaRoute,
    FromDishka,
)
from fastapi import APIRouter

from application.auth.login_handler import LoginHandler
from application.auth.register_handler import RegisterHandler
from presentation.web_api.routes.schemas import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    RegisterResponse,
)

auth_router = APIRouter(prefix="/auth", tags=["auth"], route_class=DishkaRoute)


@auth_router.post("/register")
async def register(
    payload: RegisterRequest,
    handler: FromDishka[RegisterHandler],
) -> RegisterResponse:
    user, session_token = await handler.handle(payload)
    return RegisterResponse(id=user.id, session_token=session_token)


@auth_router.post("/login")
async def login(
    payload: LoginRequest,
    handler: FromDishka[LoginHandler],
) -> LoginResponse:
    user, session_token = await handler.handle(payload)
    return LoginResponse(id=user.id, session_token=session_token)
