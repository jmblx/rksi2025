from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from application.documents.utils import get_cur_msc_datetime
from infrastructure.db.models import UserDocument
from infrastructure.db.models.document import Document

YELLOW_COLOR_PERCENTAGE = 0.1


class DocumentGateway:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, document: Document):
        self.session.add(document)
        await self.session.flush()

    async def get_by_id(self, doc_id: int):
        return await self.session.get(Document, doc_id)

    async def check_document(self, document: Document, user_id: int):
        check_doc_record = UserDocument(doc_id=document.id, user_id=user_id)
        self.session.add(check_doc_record)
        await self.session.commit()
        return {
            "id": document.id,
            "status": self.get_doc_color(document),
            "expiration_date": document.expiration_date.isoformat() + "Z",
            "created_at": document.created_at.isoformat() + "Z",
            "checked_at": check_doc_record.checked_at.isoformat() + "Z",
        }

    @staticmethod
    def get_doc_color(document):
        cur_date = get_cur_msc_datetime()

        if cur_date > document.expiration_date:
            return "red"

        total_duration = document.expiration_date - document.created_at
        elapsed = cur_date - document.created_at

        if total_duration.total_seconds() > 0 and 1 - elapsed / total_duration < YELLOW_COLOR_PERCENTAGE:
            return "yellow"

        return "green"

    async def list_doc_user(self, user_id: int):
        last_docs_subq = (
            select(
                UserDocument.doc_id,
                func.max(UserDocument.id).label("last_ud_id")
            )
            .where(UserDocument.user_id == user_id)
            .group_by(UserDocument.doc_id)
            .subquery()
        )

        query = (
            select(UserDocument, Document)
            .join(last_docs_subq, UserDocument.id == last_docs_subq.c.last_ud_id)
            .join(Document, Document.id == UserDocument.doc_id)
            .order_by(UserDocument.id.asc())
        )

        result = await self.session.execute(query)
        rows = result.all()

        return [
            {
                "document_id": row.Document.id,
                "status": self.get_doc_color(row.Document),
                "expiration_date": row.Document.expiration_date,
                "created_at": row.Document.created_at,
                "checked_at": row.UserDocument.checked_at,
            }
            for row in rows
        ]

    async def get_by_token(self, token: str):
        result = await self.session.execute(
            select(Document).where(Document.token == token)
        )
        return result.scalar()
