from __future__ import annotations

from core.command_context import CommandContext


async def help(ctx: CommandContext, message: str) -> object | None:
    help_msg = (
        "Vynia Bridge Bot » \n"
        "Creator @perished_memories | \n"
        "Source Code at Github Vaenyx/vynia-bridge-bot | \n"
        "Commands list !commands\n"
    )

    return await ctx.reply(help_msg)
