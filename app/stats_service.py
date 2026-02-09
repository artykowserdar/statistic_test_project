from typing import Optional
from uuid import UUID

from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession

from .models import UserContentStat


async def record_view(
    session: AsyncSession,
    user_token: str,
    content_type: str,
    content_id: str
) -> UserContentStat:
    stmt = (
        update(UserContentStat)
        .where(
            UserContentStat.user_token == user_token,
            UserContentStat.content_type == content_type,
            UserContentStat.content_id == content_id,
        )
        .values(
            last_visited_at=func.now(),
            view_count=UserContentStat.view_count + 1,
        )
        .returning(UserContentStat)
    )

    result = await session.execute(stmt)
    stat = result.scalar_one_or_none()

    if not stat:
        stat = UserContentStat(
            user_token=user_token,
            content_type=content_type,
            content_id=content_id,
            view_count=1,
        )
        session.add(stat)
        await session.flush()
    await session.commit()

    return stat


async def get_stat(
    session: AsyncSession,
    user_token: str,
    content_type: str,
    content_id: UUID
) -> Optional[UserContentStat]:
    result = await session.execute(
        select(UserContentStat).where(
            UserContentStat.user_token == user_token,
            UserContentStat.content_type == content_type,
            UserContentStat.content_id == content_id,
        )
    )
    return result.scalar_one_or_none()


async def update_stat_notes(
    session: AsyncSession,
    user_token: str,
    content_type: str,
    content_id: UUID,
    notes: Optional[str]
) ->  Optional[UserContentStat]:
    stmt = (
        update(UserContentStat)
        .where(
            UserContentStat.user_token == user_token,
            UserContentStat.content_type == content_type,
            UserContentStat.content_id == content_id,
        )
        .values(notes=notes)
        .returning(UserContentStat)
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()