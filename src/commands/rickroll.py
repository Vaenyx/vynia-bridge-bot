from core.command_context import CommandContext, get_name
from typing import Any


async def rickroll(ctx: CommandContext, message: str) -> Any:
    name = get_name(ctx, message)

    await ctx.minecraft.chat(fr"/t {name} https://www.youtube.com/watch?v=xvFZjo5PgG0")
    return await ctx.reply(f"Sent rickroll to {name}")
