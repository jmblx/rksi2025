import hashlib
from typing import cast

from redis.asyncio import Redis

from application.auth.common.errors import EmailCodeMismatch
from infrastructure.db.gateways.user_gateway import UserGateway
from infrastructure.token_service import TokenService
from presentation.web_api.routes.schemas import CodeToTokenCommand


class CodeToTokenHandler:
    def __init__(self, user_gateway: UserGateway, token_service: TokenService, redis: Redis):
        self.user_gateway = user_gateway
        self.token_service = token_service
        self.redis = redis

    async def handle(self, command: CodeToTokenCommand) -> tuple[str, str]:
        email = cast(str, command.email)
        stored_hash = await self.redis.get(f"email_code:{email}")

        if not stored_hash:
            raise EmailCodeMismatch

        provided_hash = hashlib.sha256(command.code.encode()).hexdigest()

        if provided_hash != stored_hash:
            raise EmailCodeMismatch

        user = await self.user_gateway.find_user_by_email(email)

        return await self.token_service.create_token_pair(user)
