# Adding Custom Commands

Commands are stored in:

```txt
src/commands/
```

## 1. Create a command file

Create a new Python file inside the commands folder.

Example:

```txt
src/commands/hello.py
```

## 2. Add the command function

Every command should be an async function with this structure:

```py
from typing import Any

from core.command_context import CommandContext


async def hello(ctx: CommandContext, message: str) -> Any:
    return await ctx.reply("Hello!")
```

The important part is:

```py
await ctx.reply(...)
```

This sends the reply back to Discord or Minecraft.

## 3. CommandContext

Every command gets a `CommandContext` object as the first parameter:

```py
async def hello(ctx: CommandContext, message: str) -> Any:
```

The context provides useful information and functions:

```py
ctx.author
```

The name of the user who executed the command.

```py
ctx.platform
```

The platform where the command was executed.

Possible values:

```txt
discord
minecraft
```

```py
ctx.reply
```

A function used to reply to the command.

Example:

```py
await ctx.reply("Hello!")
```

```py
ctx.discord
```

The Discord bot instance.

You can use this if your command needs access to Discord-specific features.

```py
ctx.minecraft
```

The Minecraft bot manager instance.

You can use this if your command needs access to Minecraft-specific features.

## 4. Using command arguments

The `message` parameter contains everything after the command name.

Example usage:

```txt
!hello this is a test
```

Then `message` will contain:

```txt
this is a test
```

Example command:

```py
from typing import Any

from core.command_context import CommandContext


async def hello(ctx: CommandContext, message: str) -> Any:
    return await ctx.reply(f"Hello {ctx.author}, you said: {message}")
```

## 5. Using APIs in commands

Commands can also call external APIs.

API helper files are stored in:

```txt
src/apis/
```

They are meant to keep API logic outside of the command file.

This keeps commands smaller and makes the same API code reusable in multiple commands.

### 5.1 Add API keys

API keys are read from environment variables.

Add your api keys in your .env file or in /etc/environment file based on `.env.example`:

```txt
BRIDGE_ACCOUNT_EMAIL=...
BRIDGE_DISCORD_TOKEN=...
BRIDGE_DISCORD_CHANNEL=...

# For commands
URCHIN_API_KEY=...
HYPIXEL_API_KEY=...
```

If a command imports an API helper and the needed key is missing, the bot should raise an error.

### 5.2 Use an existing API helper

Example using the Hypixel helper:

```py
from typing import Any

from core.command_context import CommandContext, get_name
from apis.hypixel import hypixel_get


async def level(ctx: CommandContext, message: str) -> Any:
    name = get_name(ctx, message)

    try:
        data = await hypixel_get(name)
        player = data.get("player", {})
        display_name = player.get("displayname", name)

        return await ctx.reply(f"Found Hypixel player: {display_name}")
    except Exception as e:
        return await ctx.reply(f"Error: {e}")
```

Example using the Urchin helper:

```py
from apis.urchin import urchin_get


data = await urchin_get("/player/tags", "keiyae")
```

The first argument is the Urchin endpoint.

The second argument is the player name or UUID.

### 5.3 Add a new API helper

If you want to add another API, create a new file in:

```txt
src/apis/
```

Example:

```txt
src/apis/example.py
```

Basic structure:

```py
import os
from typing import Any

import requests

from helpers.redis_cache import redis_cache

EXAMPLE_API_KEY = os.getenv("EXAMPLE_API_KEY")
if not EXAMPLE_API_KEY:
    raise RuntimeError("EXAMPLE_API_KEY was not provided")


@redis_cache(ttl=300)
async def example_get(player: str) -> dict[str, Any]:
    response = requests.get(
        "https://api.example.com/player",
        headers={"X-API-Key": EXAMPLE_API_KEY},
        params={"player": player},
        timeout=10,
    )

    data = response.json()

    if response.status_code != 200:
        raise RuntimeError(data.get("error", response.text))

    return data
```

Then use it in a command:

```py
from apis.example import example_get


data = await example_get("keiyae")
```

### 5.4 Caching API calls

API helpers can use the Redis cache decorator:

```py
from helpers.redis_cache import redis_cache


@redis_cache(ttl=300)
async def example_get(player: str) -> dict[str, Any]:
    ...
```

The `ttl` value is in seconds.

For example:

```txt
300  = 5 minutes
3600 = 1 hour
```

This is useful for commands like stats commands, because repeated calls for the same player do not have to hit the API every time.
Important: Since redis is asnyc all the functions using the cache decorator are turned into async functions (even if you define them as regular functions) so define them as such.

```txt
REDIS_URL=redis://redis:6379
```

So API caching works automatically.

## 6. Register the command

Open:

```txt
src/commands_mapping.py
```

Add the import:

```py
from commands.hello import hello
```

Then add the command to the `COMMANDS` dictionary:

```py
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
    "hello": hello,
}
```

## 7. Use the command

You can now use:

```txt
!hello
```

or:

```txt
!hello some message
```

The command name is the key in `COMMANDS`.

For example:

```py
"hello": hello
```

means the command is used like this:

```txt
!hello
```
