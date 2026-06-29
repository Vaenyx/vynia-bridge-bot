from __future__ import annotations

import traceback

import httpx

from core.command_context import CommandContext


async def get_useless_fact() -> str | None:
    try:
        async with httpx.AsyncClient(timeout=3) as client:
            res = await client.get(
                "https://uselessfacts.jsph.pl/api/v2/facts/random?language=en"
            )
            res.raise_for_status()

            data = res.json()
            return data["text"]

    except httpx.HTTPStatusError as e:
        print(f"Useless Facts API returned HTTP {e.response.status_code}: {e}")
        traceback.print_exc()
        return None

    except httpx.RequestError as e:
        print(f"Useless Facts API request failed: {e}")
        traceback.print_exc()
        return None

    except (KeyError, ValueError) as e:
        print(f"Useless Facts API returned invalid data: {e}")
        traceback.print_exc()
        return None

    except Exception as e:
        print(f"Unexpected Useless Facts API error: {e}")
        traceback.print_exc()
        return None


async def useless_fact(ctx: CommandContext, message: str) -> object | None:
    fact = await get_useless_fact()

    if fact:
        return await ctx.reply(fact)

    return await ctx.reply("No super useful fact rn")
