import hashlib
import secrets
from datetime import datetime, UTC

from application.auth.common.errors import UserNotFound, PwdMismatch
from application.common.interfaces.uow import Uow
from infrastructure.db.gateways.session_gateway import SessionGateway
from infrastructure.db.gateways.user_gateway import UserGateway
from infrastructure.db.models import UserSession


class LoginHandler:
    def __init__(self, uow: Uow, user_gateway: UserGateway, session_gateway: SessionGateway):
        self.uow = uow
        self.user_gateway = user_gateway
        self.session_gateway = session_gateway

    async def handle(self, payload):
        user = await self.user_gateway.find_user_by_email(payload.email)
        if not user:
            raise UserNotFound(by="email")

        password_hash = hashlib.sha256(payload.password.encode()).hexdigest()
        if user.password_hash != password_hash:
            raise PwdMismatch

        token = secrets.token_urlsafe(32)
        token_hash = hashlib.sha256(token.encode()).hexdigest()

        session = UserSession(
            user_id=user.id,
            session_token_hash=token_hash,
            created_at=datetime.now(tz=UTC),
        )
        await self.session_gateway.save(session)

        await self.uow.commit()
        return user, token
