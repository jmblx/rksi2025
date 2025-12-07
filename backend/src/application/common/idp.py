import hashlib
from typing import NewType

from application.auth.common.errors import UserNotFound, UnauthorizedError
from core.config import logger
from infrastructure.db.gateways.session_gateway import SessionGateway
from infrastructure.db.gateways.user_gateway import UserGateway
from infrastructure.db.models.user import User
from infrastructure.db.models.session import UserSession

SessionHash = NewType("SessionHash", str)


class IdentityProvider:
    def __init__(
        self,
        session_hash: SessionHash,
        session_gateway: SessionGateway,
        user_gateway: UserGateway,
    ):
        self.session_hash = session_hash
        self.session_gateway = session_gateway
        self.user_gateway = user_gateway

    async def get_current_user_id(self) -> int:
        if not self.session_hash:
            raise UnauthorizedError()

        logger.info(f"Raw session token: {self.session_hash}")

        hashed = hashlib.sha256(self.session_hash.encode()).hexdigest()

        session: UserSession | None = await self.session_gateway.find_session(
            session_hash=hashed
        )

        if session is None:
            raise UnauthorizedError()

        return session.user_id

    async def get_current_user(self) -> User:
        user_id: int = await self.get_current_user_id()

        user = await self.user_gateway.find_user_by_id(user_id)
        if user is None:
            raise UserNotFound(by="id")

        return user
