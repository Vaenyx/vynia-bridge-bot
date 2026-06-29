from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any, TYPE_CHECKING

from commands.bedwars.bedwars_all_time import bw, tags
from commands.bedwars.bedwars_period import bw_daily, bw_monthly, bw_weekly, bw_yearly
from commands.bored import bored_activity
from commands.chuck_norris import chuck_norris
from commands.commands import commands
from commands.dad_jokes import dad_joke
from commands.fact import useless_fact
from commands.help import help
from commands.joke import joke
from commands.meow import meow
from commands.mirror import mirror
from commands.rickroll import rickroll

if TYPE_CHECKING:
    from core.command_context import CommandContext

CommandFn = Callable[["CommandContext", str], Awaitable[Any]]

COMMANDS: dict[str, CommandFn] = {
    "help": help,
    "commands": commands,
    "meow": meow,
    "mirror": mirror,
    "rickroll": rickroll,
    "bw": bw,
    "tags": tags,
    "daily": bw_daily,
    "weekly": bw_weekly,
    "monthly": bw_monthly,
    "yearly": bw_yearly,
    "dad": dad_joke,
    "joke": joke,
    "chuck": chuck_norris,
    "fact": useless_fact,
    "bored": bored_activity,
}
