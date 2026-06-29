from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any, Literal, TYPE_CHECKING

if TYPE_CHECKING:
    from core.discord_bot import DiscordBridgeBot
    from core.minecraft_bot import MinecraftBotManager

ReplyFn = Callable[[str], Awaitable[Any]]


@dataclass(slots=True)
class CommandContext:
    author: str
    platform: Literal["discord", "minecraft"]
    reply: ReplyFn
    discord: DiscordBridgeBot
    minecraft: MinecraftBotManager


def get_name_and_res(ctx: CommandContext, message: str) -> tuple[str, str]:
    if not message.strip():
        return ctx.author, ""

    data = message.split(maxsplit=1)

    if len(data) == 1:
        return data[0], ""

    return data[0], data[1]


def get_name(ctx: CommandContext, message: str) -> str:
    return get_name_and_res(ctx, message)[0]
