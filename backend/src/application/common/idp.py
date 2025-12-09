from datetime import UTC, datetime
from typing import NewType

from application.auth.common.errors import UnauthorizedError, UserNotFoundError
from infrastructure.db.gateways.session_gateway import SessionGateway
from infrastructure.db.gateways.user_gateway import UserGateway
from infrastructure.db.models.session import UserSession
from infrastructure.db.models.user import User

RefreshToken = NewType("RefreshToken", str)
AccessToken = NewType("AccessToken", str)


class IdentityProvider:
    def __init__(
        self,
        access_token: AccessToken,
        session_gateway: SessionGateway,
        user_gateway: UserGateway,
    ):
        self.access_token = access_token
        self.session_gateway = session_gateway
        self.user_gateway = user_gateway

    async def get_current_user_id(self) -> int:
        if not self.access_token:
            raise UnauthorizedError

        session: UserSession | None = await self.session_gateway.find_by_access(
            access_token=self.access_token
        )

        now = datetime.now(UTC)
        expired = session.access_expires_at <= now
        if session is None or expired:
            raise UnauthorizedError

        return session.user_id

    async def get_current_user(self) -> User:
        user_id: int = await self.get_current_user_id()

        user = await self.user_gateway.find_user_by_id(user_id)
        if user is None:
            raise UserNotFoundError(by="id")

        return user
