from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.db.models.session import UserSession


class SessionGateway:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, session: UserSession) -> None:
        self.session.add(session)
        await self.session.flush()

    async def find_session(self, session_hash: str) -> UserSession | None:
        stmt = select(UserSession).where(
            UserSession.session_token_hash == session_hash
        )
        return (await self.session.execute(stmt)).scalar()
