from helpers.ctx import CommandContext


def get_name_and_res(ctx: CommandContext, message: str) -> tuple[str, str]:
    data = message.split(" ", maxsplit=1)

    match len(data):
        case 0:
            return ctx.author, ""
        case 1:
            return data[0], ""
        case 2:
            return data[0], data[1]
