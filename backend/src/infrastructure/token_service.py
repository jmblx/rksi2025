import secrets
from datetime import UTC, datetime, timedelta

from application.auth.common.errors import UnauthorizedError
from application.common.idp import RefreshToken
from application.common.interfaces.uow import Uow
from infrastructure.db.gateways.session_gateway import SessionGateway
from infrastructure.db.models import User, UserSession

ACCESS_TTL_MINUTES = 150000
REFRESH_TTL_DAYS = 30


class SessionService:
    def __init__(self, uow: Uow, session_gateway: SessionGateway):
        self.uow = uow
        self.session_gateway = session_gateway

    async def create_session(
        self,
        user: User,
    ) -> tuple[str, str]:
        refresh_token = secrets.token_urlsafe(48)
        access_token = secrets.token_urlsafe(48)

        expires_at = datetime.now(UTC) + timedelta(days=REFRESH_TTL_DAYS)
        access_expires_at = expires_at + timedelta(minutes=ACCESS_TTL_MINUTES)

        session = UserSession(
            user_id=user.id,
            refresh_token=refresh_token,
            access_token=access_token,
            expires_at=expires_at,
            access_expires_at=access_expires_at,
            is_active=True,
        )

        await self.session_gateway.save(session)
        await self.uow.commit()

        return refresh_token, access_token

    async def refresh_session_tokens(self, cur_refresh_token: RefreshToken) -> tuple[str, str]:
        session = await self.session_gateway.find_by_refresh(cur_refresh_token)
        if not session:
            raise UnauthorizedError

        refresh_token = secrets.token_urlsafe(48)
        access_token = secrets.token_urlsafe(48)

        expires_at = datetime.now(UTC) + timedelta(days=REFRESH_TTL_DAYS)
        access_expires_at = expires_at + timedelta(minutes=ACCESS_TTL_MINUTES)

        session.refresh_token = refresh_token
        session.access_token = access_token
        session.expires_at = expires_at
        session.access_expires_at = access_expires_at

        await self.session_gateway.save(session)
        await self.uow.commit()

        return refresh_token, access_token

    async def delete_session_by_refresh(self, refresh_token: str):
        user_session = await self.session_gateway.find_by_refresh(refresh_token)
        if not user_session:
            raise UnauthorizedError
        await self.session_gateway.delete(user_session)
        await self.uow.commit()
