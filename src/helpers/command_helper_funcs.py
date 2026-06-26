from helpers.ctx import CommandContext


def get_name_and_res(ctx: CommandContext, message: str) -> tuple[str, str]:
    if not message.strip():
        return ctx.author, ""

    data = message.split(maxsplit=1)

    if len(data) == 1:
        return data[0], ""

    return data[0], data[1]


def get_name(ctx: CommandContext, message: str) -> tuple[str, str]:
    return get_name_and_res(ctx, message)[0]
