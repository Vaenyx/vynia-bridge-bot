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

from core.command_context import CommandContext # also has some utility funcs


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

## 5. Register the command

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
    "bw-daily": bw_daily,
    "bw-weekly": bw_weekly,
    "bw-monthly": bw_monthly,
    "hello": hello,
}
```

## 6. Use the command

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

