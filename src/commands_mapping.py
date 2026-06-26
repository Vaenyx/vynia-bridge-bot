from collections.abc import Awaitable, Callable

from commands.meow import meow
from commands.mirror import mirror
from commands.rickroll import rickroll

from commands.bedwars.bedwars_all_time import bw
from commands.bedwars.bedwars_period import bw_daily, bw_weekly, bw_monthly


CommandFn = Callable[["CommandContext", str], Awaitable[None]]

COMMANDS: dict[str, CommandFn] = {
    "meow": meow,
    "mirror": mirror,
    "rickroll": rickroll,
    "bw": bw,
    "bw-daily": bw_daily,
    "bw-weekly": bw_weekly,
    "bw-monthly": bw_monthly
}
