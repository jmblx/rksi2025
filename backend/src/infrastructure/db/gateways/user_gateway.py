from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.db.models.user import User


class UserGateway:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_user_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def find_user_by_id(self, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def save(self, user: User) -> None:
        self.session.add(user)
        await self.session.flush()
