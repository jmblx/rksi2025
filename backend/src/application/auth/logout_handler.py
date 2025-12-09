from application.common.idp import RefreshToken
from infrastructure.token_service import SessionService


class InvalidateTokensHandler:
    def __init__(self, session_service: SessionService, refresh_token: RefreshToken):
        self.session_service = session_service
        self.refresh_token = refresh_token

    async def handle(self):
        await self.session_service.delete_session_by_refresh(self.refresh_token)

