from core.command_context import CommandContext
from typing import Any


async def mirror(ctx: CommandContext, message: str) -> Any:
    return await ctx.reply(message)
