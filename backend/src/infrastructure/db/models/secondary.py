from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from application.documents.utils import get_cur_msc_datetime
from infrastructure.db.models import Base


class UserDocument(Base):
    __tablename__ = "user_document"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    doc_id: Mapped[int] = mapped_column(ForeignKey("document.id"))
    checked_at: Mapped[datetime] = mapped_column(DateTime, default=get_cur_msc_datetime)
