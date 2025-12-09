from dishka.integrations.fastapi import (
    DishkaRoute,
    FromDishka,
)
from fastapi import APIRouter
from starlette import status

from application.auth.login_handler import LoginHandler
from presentation.web_api.routes.schemas import (
    LoginRequest,
)

auth_router = APIRouter(prefix="/auth", tags=["auth"], route_class=DishkaRoute)


@auth_router.post("/login", responses={
    status.HTTP_204_NO_CONTENT: {"description": "User logged in"},
    status.HTTP_401_UNAUTHORIZED: {"description": "Invalid credentials"},
})
async def login(
    payload: LoginRequest,
    handler: FromDishka[LoginHandler],
):
    await handler.handle(payload)
