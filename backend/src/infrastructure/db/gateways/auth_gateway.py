from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.db.models.session import UserSession
from infrastructure.db.models.user import User


class AuthGateway:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_user_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_user(self, email: str, password_hash: str) -> User:
        user = User(email=email, password_hash=password_hash)
        self.session.add(user)
        await self.session.flush()
        return user

    async def create_session(self, user_id: int, session_token_hash: str):
        session = UserSession(
            user_id=user_id,
            session_token_hash=session_token_hash,
            created_at=datetime.now(tz=UTC),
        )
        self.session.add(session)
