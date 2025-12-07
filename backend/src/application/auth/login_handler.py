import hashlib
import secrets

from application.auth.common.errors import UserNotFound, PwdMismatch
from application.common.interfaces.uow import Uow
from infrastructure.db.gateways.auth_gateway import AuthGateway


class LoginHandler:
    def __init__(self, uow: Uow, gateway: AuthGateway):
        self.uow = uow
        self.gateway = gateway

    async def handle(self, payload):
        user = await self.gateway.find_user_by_email(payload.email)
        if not user:
            raise UserNotFound(by="email")

        password_hash = hashlib.sha256(payload.password.encode()).hexdigest()
        if user.password_hash != password_hash:
            raise PwdMismatch

        token = secrets.token_urlsafe(32)
        token_hash = hashlib.sha256(token.encode()).hexdigest()

        await self.gateway.create_session(user.id, token_hash)

        await self.uow.commit()
        return user, token
