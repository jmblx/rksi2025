from typing import cast

from dishka.integrations.fastapi import (
    DishkaRoute,
    FromDishka,
)
from fastapi import APIRouter
from pydantic import EmailStr

from application.common.idp import IdentityProvider
from presentation.web_api.routes.schemas import MeResponse


user_router = APIRouter(prefix="/user", tags=["user"], route_class=DishkaRoute)


@user_router.get("/me")
async def get_me(identity: FromDishka[IdentityProvider]):
    user = await identity.get_current_user()
    return MeResponse(id=user.id, email=cast(EmailStr, user.email))
