from commands_mapping import COMMANDS

from core.command_context import CommandContext


async def handle_command(
    ctx: CommandContext,
    message: str,
) -> bool:
    if not message.startswith("!"):
        return False

    parts = message[1:].split(maxsplit=1)

    command = parts[0].lower()
    pruned_messaged = parts[1] if len(parts) == 2 else ""

    func = COMMANDS.get(command)

    if not func:
        return False

    print(f"{ctx.author} ({ctx.platform}) called command '{command}'")

    await func(ctx, pruned_messaged)

    return True
