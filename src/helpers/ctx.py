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
