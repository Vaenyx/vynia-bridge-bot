from typing import Any
import os

import requests

from helpers.command_helper_funcs import get_name
from helpers.ctx import CommandContext

from helpers.hypixel import stars_from_xp
from helpers.formatting import _fmt

URCHIN_BASE_URL = "https://api.urchin.gg/v3"

URCHIN_API_KEY = os.getenv("URCHIN_API_KEY")
if not URCHIN_API_KEY:
    raise RuntimeError("URCHIN_API_KEY was not provided")

URCHIN_HEADERS = {
    "X-API-Key": URCHIN_API_KEY,
}


def _urchin_get(endpoint: str, player: str) -> dict[str, Any]:
    response = requests.get(
        f"{URCHIN_BASE_URL}{endpoint}",
        headers=URCHIN_HEADERS,
        params={"player": player},
        timeout=10,
    )

    data = response.json()

    if response.status_code != 200:
        raise RuntimeError(data.get("error", response.text))

    return data


def _bw_stat(stats: dict[str, Any], key: str, default=0):
    return (
        stats.get("delta", {})
        .get("stats", {})
        .get("Bedwars", {})
        .get(key, default)
    )


def get_bw_daily(player: str) -> dict[str, Any]:
    return _urchin_get("/player/sessions/daily", player)


def get_bw_weekly(player: str) -> dict[str, Any]:
    return _urchin_get("/player/sessions/weekly", player)


def get_bw_monthly(player: str) -> dict[str, Any]:
    return _urchin_get("/player/sessions/monthly", player)


def _format_stats(title: str, player: str, stats: dict[str, Any]) -> str:
    wins = _bw_stat(stats, "wins_bedwars")
    losses = _bw_stat(stats, "losses_bedwars")

    final_kills = _bw_stat(stats, "final_kills_bedwars")
    final_deaths = _bw_stat(stats, "final_deaths_bedwars")

    beds_broken = _bw_stat(stats, "beds_broken_bedwars")
    beds_lost = _bw_stat(stats, "beds_lost_bedwars")

    kills = _bw_stat(stats, "kills_bedwars")
    deaths = _bw_stat(stats, "deaths_bedwars")

    games = _bw_stat(stats, "games_played_bedwars")

    fkdr = final_kills / max(1, final_deaths)
    wlr = wins / max(1, losses)
    bblr = beds_broken / max(1, beds_lost)
    kdr = kills / max(1, deaths)

    xp_gained = _bw_stat(stats, "Experience")
    stars_gained = stars_from_xp(xp_gained)

    return (
        f"{player.lower()} ({title}) » "
        f"+{_fmt(stars_gained)}✫ | "
        f"FKDR {_fmt(fkdr)} | "
        f"WLR {_fmt(wlr)} | "
        f"BBLR {_fmt(bblr)} | "
        f"KDR {_fmt(kdr)} | "
        f"{games} games"
    )


async def bw_daily(ctx: CommandContext, message: str) -> Any:
    name = get_name(ctx, message)

    try:
        stats = get_bw_daily(name)
        return await ctx.reply(_format_stats("Daily", name, stats))
    except Exception as e:
        return await ctx.reply(f"Error: {e}")


async def bw_weekly(ctx: CommandContext, message: str) -> Any:
    name = get_name(ctx, message)

    try:
        stats = get_bw_weekly(name)
        return await ctx.reply(_format_stats("Weekly", name, stats))
    except Exception as e:
        return await ctx.reply(f"Error: {e}")


async def bw_monthly(ctx: CommandContext, message: str) -> Any:
    name = get_name(ctx, message)

    try:
        stats = get_bw_monthly(name)
        return await ctx.reply(_format_stats("Monthly", name, stats))
    except Exception as e:
        return await ctx.reply(f"Error: {e}")
