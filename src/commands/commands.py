from typing import Any

from core.command_context import CommandContext


async def commands(ctx: CommandContext, message: str) -> Any:
    from commands_mapping import COMMANDS

    command_names = " ".join(f"!{name}" for name in sorted(COMMANDS))
    return await ctx.reply(f"Commands: {command_names}")
