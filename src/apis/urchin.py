from __future__ import annotations

from typing import Any
import os
import requests

from helpers.redis_cache import redis_cache

URCHIN_BASE_URL = "https://api.urchin.gg/v3"

URCHIN_API_KEY = os.getenv("URCHIN_API_KEY")
if not URCHIN_API_KEY:
    raise RuntimeError("URCHIN_API_KEY was not provided")

URCHIN_HEADERS: dict[str, str] = {
    "X-API-Key": URCHIN_API_KEY,
}


@redis_cache(ttl=300)
async def urchin_get(endpoint: str, player: str) -> dict[str, Any]:
    response = requests.get(
        f"{URCHIN_BASE_URL}{endpoint}",
        headers=URCHIN_HEADERS,
        params={"player": player},
        timeout=10,
    )

    if response.status_code == 204 or not response.text:
        data: dict[str, Any] = {}
    else:
        data = response.json()

    if response.status_code != 200:
        raise RuntimeError(
            data.get("error", response.text or f"HTTP {response.status_code}"))

    return data
