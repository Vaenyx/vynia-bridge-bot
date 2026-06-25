from collections.abc import Callable, Awaitable
from typing import Literal
from dataclasses import dataclass


ReplyFn = Callable[[str], Awaitable[None]]


@dataclass(slots=True)
class CommandContext:
    author: str
    platform: Literal["discord", "minecraft"]

    reply: ReplyFn
