import hashlib
import secrets
import threading
from datetime import datetime, UTC
from typing import cast

from redis.asyncio import Redis

from application.common.interfaces.uow import Uow
from infrastructure.db.gateways.session_gateway import SessionGateway
from infrastructure.db.gateways.user_gateway import UserGateway
from infrastructure.db.models import User
from infrastructure.email_notification import EmailCodeService
from presentation.web_api.routes.schemas import LoginRequest


class LoginHandler:
    def __init__(
        self,
        uow: Uow,
        user_gateway: UserGateway,
        session_gateway: SessionGateway,
        email_code_service: EmailCodeService,
        redis: Redis,
    ):
        self.uow = uow
        self.user_gateway = user_gateway
        self.session_gateway = session_gateway
        self.email_code_service = email_code_service
        self.redis = redis

    async def handle(self, payload: LoginRequest):
        email = cast(str, payload.email)
        user = await self.user_gateway.find_user_by_email(email)
        if not user:
            user = User(email=email)
            await self.user_gateway.save(user)

        code = f"{secrets.randbelow(10000):04d}"

        t = threading.Thread(target=self.email_code_service.send_code, args=(email, code))
        t.start()

        hashed = hashlib.sha256(code.encode()).hexdigest()
        await self.redis.set(f"email_code:{email}", hashed, ex=600)

        await self.uow.commit()
