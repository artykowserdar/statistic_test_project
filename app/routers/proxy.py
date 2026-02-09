from fastapi import APIRouter, Depends, Header, HTTPException

from ..proxy_service import proxy_request
from ..stats_service import record_view
from ..database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/api/v1", tags=["proxy"])


def extract_token(authorization: str = Header(...)) -> str:
    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "Ожидается заголовок Authorization: Bearer <token>")
    return authorization.removeprefix("Bearer ").strip()


@router.get("/allah-names/")
async def list_allah_names(token: str = Depends(extract_token)):
    return await proxy_request("GET", "allah-names/", token)


@router.get("/allah-names/{content_id}")
async def get_allah_name(
        content_id: str,  # ← было int → стало str
        token: str = Depends(extract_token),
        db: AsyncSession = Depends(get_db)
):
    data = await proxy_request("GET", f"allah-names/{content_id}", token)
    await record_view(db, token, "allah_name", content_id)
    return data


@router.post("/allah-names/{content_id}/view")
async def view_allah_name(
        content_id: str,  # ← str
        token: str = Depends(extract_token),
        db: AsyncSession = Depends(get_db)
):
    data = await proxy_request("POST", f"allah-names/{content_id}/view", token, json={})
    await record_view(db, token, "allah_name", content_id)
    return data
