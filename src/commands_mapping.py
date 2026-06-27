from collections.abc import Awaitable, Callable

from commands.meow import meow
from commands.mirror import mirror
from commands.rickroll import rickroll
from commands.dad_jokes import dad_joke
from commands.joke import joke
from commands.chuck_norris import chuck_norris
from commands.fact import useless_fact
from commands.bored import bored_activity

from commands.bedwars.bedwars_all_time import bw, tags
from commands.bedwars.bedwars_period import bw_daily, bw_weekly, bw_monthly, bw_yearly


CommandFn = Callable[["CommandContext", str], Awaitable[None]]

COMMANDS: dict[str, CommandFn] = {
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
