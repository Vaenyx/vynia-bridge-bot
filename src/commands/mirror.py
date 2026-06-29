from __future__ import annotations

from core.command_context import CommandContext


async def mirror(ctx: CommandContext, message: str) -> object | None:
    return await ctx.reply(message)
