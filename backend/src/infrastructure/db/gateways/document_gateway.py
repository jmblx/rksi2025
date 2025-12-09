from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.db.models.document import Document


class DocumentGateway:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, document: Document):
        self.session.add(document)
        await self.session.flush()
