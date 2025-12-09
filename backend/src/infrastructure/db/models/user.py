from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Integer,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from infrastructure.db.models import Base, UserSession


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    sessions = relationship(
        "UserSession",
        order_by=UserSession.created_at,
        back_populates="user",
        cascade="all, delete-orphan",
        uselist=True,
    )
