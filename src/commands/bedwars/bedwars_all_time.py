from typing import Any
import os
import requests

from core.command_context import CommandContext, get_name

from helpers.hypixel import stars_from_xp
from helpers.formatting import _fmt


HYPIXEL_API_KEY = os.getenv("HYPIXEL_API_KEY")
if not HYPIXEL_API_KEY:
    raise RuntimeError("HYPIXEL_API_KEY was not provided")


def _hypixel_get(player: str) -> dict[str, Any]:
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


def get_bw_overall(player: str) -> dict[str, Any]:
    return _hypixel_get(player)


async def bw(ctx: CommandContext, message: str) -> Any:
    name = get_name(ctx, message)

    try:
        stats = get_bw_overall(name)

        bw = (
            stats.get("player", {})
            .get("stats", {})
            .get("Bedwars", {})
        )

        wins = bw.get("wins_bedwars", 0)
        losses = bw.get("losses_bedwars", 0)

        final_kills = bw.get("final_kills_bedwars", 0)
        final_deaths = bw.get("final_deaths_bedwars", 0)

        beds_broken = bw.get("beds_broken_bedwars", 0)
        beds_lost = bw.get("beds_lost_bedwars", 0)

        kills = bw.get("kills_bedwars", 0)
        deaths = bw.get("deaths_bedwars", 0)

        games = bw.get("games_played_bedwars", 0)

        xp = bw.get("Experience", 0)
        stars = stars_from_xp(xp)

        fkdr = final_kills / max(1, final_deaths)
        wlr = wins / max(1, losses)
        bblr = beds_broken / max(1, beds_lost)
        kdr = kills / max(1, deaths)

        return await ctx.reply(
            f"{name.lower()} » "
            f"{_fmt(stars)}✫ | "
            f"FKDR {_fmt(fkdr)} | "
            f"WLR {_fmt(wlr)} | "
            f"BBLR {_fmt(bblr)} | "
            f"KDR {_fmt(kdr)} | "
            f"{games} games"
        )
    except Exception as e:
        return await ctx.reply(f"Error: {e}")
