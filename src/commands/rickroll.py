from helpers.ctx import CommandContext
from typing import Any

from helpers.command_helper_funcs import get_name


async def rickroll(ctx: CommandContext, message: str) -> Any:
    name = get_name(ctx, message)

    await ctx.minecraft.chat(fr"/t {name} https://www.youtube.com/watch?v=xvFZjo5PgG0")
    return await ctx.reply(f"Sent rickroll to {name}")
