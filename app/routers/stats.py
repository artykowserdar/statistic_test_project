from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from ..database import get_db
from ..stats_service import get_stat, update_stat_notes
from ..schemas import ContentStatRead, ContentStatUpdate
from ..routers.proxy import extract_token
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/api/stats", tags=["statistics"])


@router.get("/content/{content_type}/{content_id}", response_model=ContentStatRead)
async def get_content_statistics(
        content_type: str,
        content_id: str,  # ← было int → стало str
        token: str = Depends(extract_token),
        db: AsyncSession = Depends(get_db)
):
    if content_type not in {"goal", "dua", "allah_name"}:
        raise HTTPException(400, "content_type должен быть: goal, dua или allah_name")

    stat = await get_stat(db, token, content_type, UUID(content_id))
    if stat is None:
        raise HTTPException(404, "Статистика по этому элементу ещё не собиралась")

    return stat


@router.patch("/content/{content_type}/{content_id}", response_model=ContentStatRead)
async def update_notes(
        content_type: str,
        content_id: str,  # ← str
        body: ContentStatUpdate,
        token: str = Depends(extract_token),
        db: AsyncSession = Depends(get_db)
):
    if content_type not in {"goal", "dua", "allah_name"}:
        raise HTTPException(400, "Недопустимый content_type")

    updated = await update_stat_notes(db, token, content_type, UUID(content_id), body.notes)
    if updated is None:
        raise HTTPException(404, "Запись не найдена")

    return updated
