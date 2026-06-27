from typing import Any

from core.command_context import CommandContext

import traceback

import httpx


async def get_dad_joke() -> str | None:
    try:
        async with httpx.AsyncClient(timeout=3) as client:
            res = await client.get(
                "https://icanhazdadjoke.com/",
                headers={"Accept": "application/json"},
            )
            res.raise_for_status()

            data = res.json()
            return data["joke"]

    except httpx.HTTPStatusError as e:
        print(f"Dad joke API returned HTTP {e.response.status_code}: {e}")
        traceback.print_exc()
        return None

    except httpx.RequestError as e:
        print(f"Dad joke API request failed: {e}")
        traceback.print_exc()
        return None

    except (KeyError, ValueError) as e:
        print(f"Dad joke API returned invalid data: {e}")
        traceback.print_exc()
        return None

    except Exception as e:
        print(f"Unexpected error: {e}")
        traceback.print_exc()
        return None


async def dad_joke(ctx: CommandContext, message: str) -> Any:
    joke = await get_dad_joke()

    if joke:
        return await ctx.reply(joke)

    return await ctx.reply("No dad joke rn")
