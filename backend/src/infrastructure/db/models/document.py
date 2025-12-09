import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.db.models import Base


class Document(Base):
    __tablename__ = "document"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at : Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, default=datetime.datetime.now)
    expiration_date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    hash: Mapped[str] = mapped_column(String(64), nullable=False)
