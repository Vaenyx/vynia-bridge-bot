import asyncio

from core.discord_bot import DiscordBridgeBot
from core.config import DiscordConfig
bot = DiscordBridgeBot()


async def main():
    async with bot:
        await bot.start(DiscordConfig.token)

try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
