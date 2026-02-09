import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import String, DateTime, Text, func, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class UserContentStat(Base):
    __tablename__ = "user_content_stats"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_token: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    content_type: Mapped[str] = mapped_column(String(32), nullable=False)  # goal / dua / allah_name
    content_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)  # ← здесь изменение!
    last_visited_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    view_count: Mapped[int] = mapped_column(default=0, nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    __table_args__ = (
        UniqueConstraint("user_token", "content_type", "content_id", name="uq_user_content"),
    )