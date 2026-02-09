from datetime import datetime
from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ContentStatBase(BaseModel):
    content_type: Literal["goal", "dua", "allah_name"]
    content_id: UUID  # UUID в виде строки


class ContentStatRead(ContentStatBase):
    id: int
    user_token: str
    last_visited_at: Optional[datetime] = None
    view_count: int = 0
    notes: Optional[str] = None

    class Config:
        from_attributes = True


class ContentStatUpdate(BaseModel):
    notes: Optional[str] = Field(None, max_length=2000)


class ErrorResponse(BaseModel):
    detail: str