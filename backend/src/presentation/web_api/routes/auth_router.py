from dishka.integrations.fastapi import (
    DishkaRoute,
    FromDishka,
)
from fastapi import APIRouter
from fastapi.responses import ORJSONResponse
from starlette import status
from starlette.responses import Response

from application.auth.code_to_token_handler import CodeToTokenHandler
from application.auth.login_handler import LoginHandler
from presentation.web_api.response_utils import set_tokens
from presentation.web_api.routes.schemas import (
    LoginRequest, CodeToTokenCommand,
)

auth_router = APIRouter(prefix="/auth", tags=["auth"], route_class=DishkaRoute)


@auth_router.post("/login", responses={
    status.HTTP_204_NO_CONTENT: {"description": "Send confirmation code to email"},
    status.HTTP_401_UNAUTHORIZED: {"description": "Invalid credentials"},
})
async def login(
    payload: LoginRequest,
    handler: FromDishka[LoginHandler],
):
    await handler.handle(payload)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@auth_router.post("/confirm-login")
async def confirm_login(command: CodeToTokenCommand, handler: FromDishka[CodeToTokenHandler]):
    refresh_token, access_token = await handler.handle(command)
    response = ORJSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)
    set_tokens(response, refresh_token, access_token)
    return response
