from typing import Any
import traceback

import httpx

from core.command_context import CommandContext


async def get_chuck_norris_joke() -> str | None:
    try:
        async with httpx.AsyncClient(timeout=3) as client:
            res = await client.get("https://api.chucknorris.io/jokes/random")
            res.raise_for_status()

            data = res.json()
            return data["value"]

    except httpx.HTTPStatusError as e:
        print(f"Chuck Norris API returned HTTP {e.response.status_code}: {e}")
        traceback.print_exc()
        return None

    except httpx.RequestError as e:
        print(f"Chuck Norris API request failed: {e}")
        traceback.print_exc()
        return None

    except (KeyError, ValueError) as e:
        print(f"Chuck Norris API returned invalid data: {e}")
        traceback.print_exc()
        return None

    except Exception as e:
        print(f"Unexpected Chuck Norris API error: {e}")
        traceback.print_exc()
        return None


async def chuck_norris(ctx: CommandContext, message: str) -> Any:
    joke = await get_chuck_norris_joke()

    if joke:
        return await ctx.reply(joke)

    return await ctx.reply("No Chuck Norris joke rn")
