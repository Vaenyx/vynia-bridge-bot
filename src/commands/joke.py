from __future__ import annotations

import traceback

import httpx

from core.command_context import CommandContext


async def get_joke_api_joke() -> str | None:
    try:
        async with httpx.AsyncClient(timeout=3) as client:
            res = await client.get(
                "https://v2.jokeapi.dev/joke/Any?safe-mode&type=single"
            )
            res.raise_for_status()

            data = res.json()
            return data["joke"]

    except httpx.HTTPStatusError as e:
        print(f"JokeAPI returned HTTP {e.response.status_code}: {e}")
        traceback.print_exc()
        return None

    except httpx.RequestError as e:
        print(f"JokeAPI request failed: {e}")
        traceback.print_exc()
        return None

    except (KeyError, ValueError) as e:
        print(f"JokeAPI returned invalid data: {e}")
        traceback.print_exc()
        return None

    except Exception as e:
        print(f"Unexpected JokeAPI error: {e}")
        traceback.print_exc()
        return None


async def joke(ctx: CommandContext, message: str) -> object | None:
    joke = await get_joke_api_joke()

    if joke:
        return await ctx.reply(joke)

    return await ctx.reply("No joke rn")
