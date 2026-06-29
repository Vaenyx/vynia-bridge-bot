from __future__ import annotations

from core.command_context import CommandContext, get_name


async def rickroll(ctx: CommandContext, message: str) -> object | None:
    name = get_name(ctx, message)

    await ctx.minecraft.chat(fr"/t {name} https://www.youtube.com/watch?v=xvFZjo5PgG0")
    return await ctx.reply(f"Sent rickroll to {name}")
