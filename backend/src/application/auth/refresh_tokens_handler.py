from application.common.idp import RefreshToken
from infrastructure.token_service import SessionService


class RefreshTokensHandler:
    def __init__(self, session_service: SessionService, refresh_token: RefreshToken):
        self.session_service = session_service
        self.refresh_token = refresh_token

    async def handle(self):
        return await self.session_service.refresh_session_tokens(self.refresh_token)
