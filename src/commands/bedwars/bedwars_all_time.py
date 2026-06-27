from typing import Any

from core.command_context import CommandContext, get_name

from apis.urchin import urchin_get
from apis.hypixel import hypixel_get
from helpers.hypixel import stars_from_xp
from helpers.formatting import _fmt


async def get_bw_overall(player: str) -> dict[str, Any]:
    return await hypixel_get(player)


async def get_player_tags(player: str) -> dict[str, Any]:
    return await urchin_get("/player/tags", player)


def _format_tags(data: dict[str, Any]) -> str:
    tags = data.get("tags", [])

    if not tags:
        return "no tags"

    formatted = []

    for tag in tags[:3]:
        tag_type = tag.get("tag_type", "tag")
        reason = tag.get("reason")

        if reason:
            formatted.append(f"{tag_type}: {reason}")
        else:
            formatted.append(tag_type)

    if len(tags) > 3:
        formatted.append(f"+{len(tags) - 3} more")

    return " | ".join(formatted)


async def tags(ctx: CommandContext, message: str) -> Any:
    name = get_name(ctx, message)

    try:
        tag_data = await get_player_tags(name)
        tags_text = _format_tags(tag_data)

        return await ctx.reply(
            f"{name.lower()} » "
            f"Tags: {tags_text}"
        )
    except Exception as e:
        return await ctx.reply(f"Error: {e}")


async def bw(ctx: CommandContext, message: str) -> Any:
    name = get_name(ctx, message)

    try:
        stats = await get_bw_overall(name)

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

        tag_data = await get_player_tags(name)
        tags_text = _format_tags(tag_data)

        return await ctx.reply(
            f"{name.lower()} » "
            f"{_fmt(stars)}✫ | "
            f"FKDR {_fmt(fkdr)} | "
            f"WLR {_fmt(wlr)} | "
            f"BBLR {_fmt(bblr)} | "
            f"KDR {_fmt(kdr)} | "
            f"{games} games | "
            f"Tags: {tags_text}"
        )
    except Exception as e:
        return await ctx.reply(f"Error: {e}")
