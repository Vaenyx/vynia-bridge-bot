from typing import Any
import traceback

import httpx

from core.command_context import CommandContext


async def get_bored_activity() -> str | None:
    try:
        async with httpx.AsyncClient(timeout=3) as client:
            res = await client.get("https://bored-api.appbrewery.com/random")
            res.raise_for_status()

            data = res.json()
            return data["activity"]

    except httpx.HTTPStatusError as e:
        print(f"Bored API returned HTTP {e.response.status_code}: {e}")
        traceback.print_exc()
        return None

    except httpx.RequestError as e:
        print(f"Bored API request failed: {e}")
        traceback.print_exc()
        return None

    except (KeyError, ValueError) as e:
        print(f"Bored API returned invalid data: {e}")
        traceback.print_exc()
        return None

    except Exception as e:
        print(f"Unexpected Bored API error: {e}")
        traceback.print_exc()
        return None


async def bored_activity(ctx: CommandContext, message: str) -> Any:
    activity = await get_bored_activity()

    if activity:
        return await ctx.reply(activity)

    return await ctx.reply("You may relax")
