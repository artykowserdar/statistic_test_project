import httpx
from fastapi import HTTPException
from typing import Optional, Union, Dict, List, Any

from .config import settings


async def proxy_request(
    method: str,
    path: str,
    token: str,
    json: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None,
) -> Optional[Union[Dict[str, Any], List[Any]]]:
    url = f"{settings.external_api_base.rstrip('/')}/{path.lstrip('/')}"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "User-Agent": "StatisticTestProxy/1.0",
    }

    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            resp = await client.request(
                method=method.upper(),
                url=url,
                headers=headers,
                json=json,
                params=params,
            )

            if resp.status_code >= 400:
                try:
                    error_data = resp.json()
                    detail = error_data.get("detail", resp.text[:400])
                except:
                    detail = resp.text[:400] or f"HTTP {resp.status_code}"
                raise HTTPException(status_code=resp.status_code, detail=detail)

            if resp.status_code in (204, 304) or not resp.content:
                return None

            try:
                return resp.json()
            except httpx.JSONDecodeError:
                raise HTTPException(
                    status_code=502,
                    detail=f"Сервер вернул не-JSON (Content-Type: {resp.headers.get('content-type')}, начало: {resp.text[:200]!r})"
                )

        except httpx.TimeoutException:
            raise HTTPException(504, "Внешний API не отвечает (таймаут)")
        except Exception as exc:
            raise HTTPException(502, f"Ошибка прокси: {str(exc)}")