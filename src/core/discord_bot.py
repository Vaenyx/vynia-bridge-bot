import traceback

import aiohttp
import discord
from discord.ext import commands

from core.config import DiscordConfig
from core.minecraft_bot import MinecraftBotManager
from core.commands_handler import handle_command
from core.command_context import CommandContext

from helpers.censor import censor
from helpers.guild_keywords import GUILD_KEYWORDS


class DiscordBridgeBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or(DiscordConfig.prefix),
            allowed_mentions=discord.AllowedMentions(everyone=False), intents=discord.Intents(
                guild_messages=True, message_content=True, guilds=True, members=True,
            ),
            help_command=None,
            activity=discord.Game(name="Guild Bridge Bot"),
        )
        self.owner_id = DiscordConfig.ownerId
        self.mineflayer_bot = None
        self.add_check(self.ready_check)

    async def ready_check(self, ctx) -> bool:
        return self.is_ready() and self.mineflayer_bot.is_ready()

    async def on_error(self, event_method: str, /, *args, **kwargs):
        lines = [
            f"An error occurred in {event_method} with args {
                args} and kwargs {kwargs}:",
            *traceback.format_exc().splitlines()
        ]
        for line in lines:
            print(f"Discord > [ERROR] {line}")

    async def on_ready(self):
        print(f"Discord > Bot Running as {self.user}")
        channel = self.get_channel(DiscordConfig.channel)
        if not channel:
            print(
                f"Discord > Channel {
                    DiscordConfig.channel} not found! Please set the correct channel ID!"
            )
            return await self.close()

        if not self.mineflayer_bot:
            print("Discord > Starting the Minecraft bot...")
            try:
                self.mineflayer_bot = MinecraftBotManager.createbot(self)
            except Exception as e:
                print(f"Discord > Failed to start Minecraft bot: {e}")
                traceback.print_exc()
                return await self.close()

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.channel.id != DiscordConfig.channel:
            return

        ctx = CommandContext(
            author=message.author.display_name,
            platform="discord",
            reply=message.channel.send,
            discord=self,
            minecraft=self.mineflayer_bot
        )

        if await handle_command(ctx, message.content):
            return

        await self.mineflayer_bot.send_minecraft_message(
            message.author.display_name,
            message.content,
        )

    async def on_command(self, ctx):
        print(f"Discord > Command {
              ctx.command} has been invoked by {ctx.author}")

    async def close(self):
        print(f"Discord > Bot {self.user} is shutting down...")
        if self.mineflayer_bot is not None:
            print("Discord > Stopping Minecraft bot...")
            self.mineflayer_bot.stop(False)
            print("Discord > Minecraft bot has been stopped.")
        await super().close()

    async def send_message(self, *args, **kwargs):
        kwargs["allowed_mentions"] = discord.AllowedMentions.none()

        if not args and "content" not in kwargs and "embed" not in kwargs:
            print("Discord > [WARNING] Attempted to send an empty message")
            return

        channel = self.get_channel(DiscordConfig.channel)
        if channel is None:
            return

        try:
            return await channel.send(*args, **kwargs)
        except aiohttp.ClientError:
            return

    async def send_user_message(self, username, message):
        return await self.send_message(
            content=f"G > {username}: {
                discord.utils.escape_markdown(message)}"
        )

    async def send_minecraft_user_message(self, username, message: discord.Message):
        content = censor(message.content).strip()

        if not content:
            if message.attachments:
                count = len(message.attachments)
                await self.mineflayer_bot.chat(
                    f"/gc {username}: attached {'a' if count ==
                                                1 else count} file{'s' if count > 1 else ''}"
                )
            return

        if message.reference:
            if message.reference.cached_message:
                reply = message.reference.cached_message
            else:
                reply = None
                try:
                    reply = await message.channel.fetch_message(message.reference.message_id)
                except discord.HTTPException:
                    pass

            if not reply:
                return

            if reply.author != self.user:
                reply_to = "@" + reply.author.name
            else:
                reply_to = None

                if reply.embeds[0].description:
                    try:
                        reply_to = reply.embeds[0].author.name
                    except AttributeError:
                        reply_to = "unkown (bot probably)"
            if reply_to:
                username += f" replied to {reply_to}"

        content = f"/gc {username}: {content}"
        content = content.encode("utf-8").decode("unicode-escape")
        content = content.encode("ascii", "ignore").decode("ascii")

        if len(content) > 256:
            content = content[:253] + "..."

        await self.mineflayer_bot.chat(content)

    async def send_discord_message(self, message):
        if not message or f"{self.mineflayer_bot.bot.name}:" in message:
            return

        if not message.startswith("Guild > "):
            return

        message = censor(message).replace("Guild > ", "", 1)

        await self.send_message(content=message)

        if any(keyword in message for keyword in GUILD_KEYWORDS):
            await self.send_message(content=message)
