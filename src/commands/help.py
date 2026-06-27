from core.command_context import CommandContext
from typing import Any


async def help(ctx: CommandContext, message: str) -> Any:
    help_msg = (
        "Vynia Bridge Bot » \n"
        "Creator @perished_memories | \n"
        "Source Code at Github Vaenyx/vynia-bridge-bot | \n"
        "Commands list !commandso\n"
    )

    return await ctx.reply(help_msg)
