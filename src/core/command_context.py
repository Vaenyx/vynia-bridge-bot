from collections.abc import Callable, Awaitable
from typing import Literal, TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from core.discord_bot import DiscordBridgeBot
    from core.minecraft_bot import MinecraftBotManager

ReplyFn = Callable[[str], Awaitable[None]]


@dataclass(slots=True)
class CommandContext:
    author: str
    platform: Literal["discord", "minecraft"]

    reply: ReplyFn

    discord: "DiscordBridgeBot"
    minecraft: "MinecraftBotManager"


def get_name_and_res(ctx: CommandContext, message: str) -> tuple[str, str]:
    if not message.strip():
        return ctx.author, ""

    data = message.split(maxsplit=1)

    if len(data) == 1:
        return data[0], ""

    return data[0], data[1]


def get_name(ctx: CommandContext, message: str) -> tuple[str, str]:
    return get_name_and_res(ctx, message)[0]
