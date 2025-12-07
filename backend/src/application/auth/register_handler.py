import hashlib
import secrets

from application.auth.common.errors import EmailAlreadyRegistered
from application.common.interfaces.uow import Uow
from infrastructure.db.gateways.auth_gateway import AuthGateway


class RegisterHandler:
    def __init__(self, uow: Uow, gateway: AuthGateway):
        self.uow = uow
        self.gateway = gateway

    async def handle(self, payload):
        exists = await self.gateway.find_user_by_email(payload.email)
        if exists:
            raise EmailAlreadyRegistered

        password_hash = hashlib.sha256(payload.password.encode()).hexdigest()

        user = await self.gateway.create_user(
            email=payload.email,
            password_hash=password_hash,
        )

        token = secrets.token_urlsafe(32)
        token_hash = hashlib.sha256(token.encode()).hexdigest()

        await self.gateway.create_session(user.id, token_hash)

        await self.uow.commit()
        return user, token
