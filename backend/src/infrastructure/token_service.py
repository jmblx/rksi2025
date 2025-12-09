import secrets
from datetime import datetime, timedelta, UTC

from application.common.interfaces.uow import Uow
from infrastructure.db.models import User, UserSession
from infrastructure.db.gateways.session_gateway import SessionGateway


ACCESS_TTL_MINUTES = 150000
REFRESH_TTL_DAYS = 30


class TokenService:
    def __init__(self, uow: Uow, session_gateway: SessionGateway):
        self.uow = uow
        self.session_gateway = session_gateway

    async def create_token_pair(self, user: User) -> tuple[str, str]:
        access_token = secrets.token_urlsafe(48)
        refresh_token = secrets.token_urlsafe(48)

        expires_at = datetime.now(UTC) + timedelta(days=REFRESH_TTL_DAYS)

        session = UserSession(
            user_id=user.id,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=expires_at,
            is_active=True,
        )

        await self.session_gateway.save(session)

        await self.uow.commit()

        return refresh_token, access_token
