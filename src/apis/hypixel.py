import os
import requests
from typing import Any

from helpers.redis_cache import redis_cache

HYPIXEL_API_KEY = os.getenv("HYPIXEL_API_KEY")
if not HYPIXEL_API_KEY:
    raise RuntimeError("HYPIXEL_API_KEY was not provided")


@redis_cache(ttl=3600)
def hypixel_get(player: str) -> dict[str, Any]:
    response = requests.get(
        "https://api.hypixel.net/v2/player",
        headers={"API-Key": HYPIXEL_API_KEY},
        params={"name": player},
        timeout=10,
    )

    data = response.json()

    if response.status_code != 200:
        raise RuntimeError(data.get("cause", response.text))

    if not data.get("success", False):
        raise RuntimeError(data.get("cause", "Unknown Hypixel API error"))

    return data
