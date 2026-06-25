from core.config import AccountConfig, ServerConfig
import asyncio
import json
import time
import traceback
import javascript

from core.commands import handle_command
from helpers.ctx import CommandContext


class MinecraftBotManager:
    def __init__(self, client, bot):
        self.client = client
        self.bot = bot

        self._message_block = None
        self.auto_restart = True

        self._online = False
        self._starting = False

    def is_ready(self):
        return self._online and not self._starting

    def is_online(self):
        return self._online

    def is_starting(self):
        return self._starting

    async def chat(self, message):
        print(message)
        self.bot.chat(message)

    def stop(self, restart: bool = True):
        print("Minecraft > Stopping bot...")

        self._starting = restart
        self._online = False

        self.client.mineflayer_bot = None

        javascript.terminate()

        if not restart:
            return

        time.sleep(3)

        print("Minecraft > Restarting...")

        try:
            self.createbot(self.client)
        except Exception as e:
            print(f"Minecraft > Error: {e}")
            traceback.print_exc()
            raise

    def send_to_discord(self, message: str):
        asyncio.run_coroutine_threadsafe(
            self.client.send_discord_message(message),
            self.client.loop,
        )

    def _clear_message_block(self):
        self._message_block = None

    def _start_message_block(self):
        self._message_block = {
            "started": time.monotonic(),
            "lines": [],
        }

    def _append_message_block(self, message: str):
        self._message_block["lines"].append(message)

    def _flush_message_block(self):
        self.send_to_discord("\n".join(self._message_block["lines"]))
        self._clear_message_block()

    def _message_block_expired(self) -> bool:
        return (
            self._message_block is not None
            and time.monotonic() - self._message_block["started"] > 10
        )

    def oncommands(self):
        @javascript.On(self.bot, "spawn")
        def login():
            if not self._online:
                print("Minecraft > Bot is logged in as", self.bot.username)

            self._online = True

            self.client.dispatch("minecraft_ready")

            time.sleep(3)
            self.bot.chat("/limbo")

        @javascript.On(self.bot, "end")
        def end(reason):
            time.sleep(3)

            print(f"Minecraft > Bot offline: {reason}")

            self.client.dispatch("minecraft_disconnected")

            self.stop(self.auto_restart)

        @javascript.On(self.bot, "kicked")
        def kicked(reason, loggedIn):
            if isinstance(reason, str):
                try:
                    reason = json.loads(reason)
                except Exception:
                    reason_text = reason
                else:
                    reason_text = reason.get("text", "") + "".join(
                        e.get("text", "") for e in reason.get("extra", [])
                    )
            else:
                reason_text = reason.get("text", "") + "".join(
                    e.get("text", "") for e in reason.get("extra", [])
                )

            print(f"Minecraft > Bot kicked: {reason_text}")

            self.client.dispatch("minecraft_disconnected")

            if loggedIn:
                self.send_to_discord("Bot kicked from the server.")
                self.stop(True)
            else:
                self.send_to_discord(
                    "Bot kicked before logging in to the server.")
                self.stop(False)

        @javascript.On(self.bot, "error")
        def error(reason):
            print(reason)
            self.client.dispatch("minecraft_error")

        @javascript.On(self.bot, "messagestr")
        def chat(message, _, raw_message, *args):
            prefix = "Guild > "
            if message.startswith(f"{prefix}{self.bot.username}"):
                return

            elif message.startswith(prefix):
                sender, _, content = message.removeprefix(
                    prefix).partition(": ")

                username = sender.split()[-1]

                async def reply(text: str):
                    await self.chat(f"/t {username} {text}"[:256])

                ctx = CommandContext(
                    author=username,
                    platform="minecraft",
                    reply=reply,
                    discord=self.client,
                    minecraft=self
                )

                future = asyncio.run_coroutine_threadsafe(
                    handle_command(ctx, content),
                    self.client.loop,
                )
                try:
                    if future.result():
                        return
                except Exception:
                    traceback.print_exc()

            if self._message_block_expired():
                self._clear_message_block()

            if self._message_block:
                if (
                    message.startswith("----------")
                    or message.endswith("----------")
                ):
                    self._flush_message_block()
                    return

                self._append_message_block(message)
                return

            if (
                message.startswith("-----")
                and message.endswith("-----")
            ):
                self._start_message_block()
                return

            self.send_to_discord(message)

    def send_minecraft_message(self, discord, message):
        message_text = f"/gc {discord}: {message}"
        message_text = message_text[:256]
        self.bot.chat(message_text)

    def send_minecraft_command(self, message):
        message = message.replace("!o ", "/")
        self.bot.chat(message)

    # add types
    @classmethod
    def createbot(cls, client):
        javascript.init()

        mineflayer = javascript.require("mineflayer")

        print("Minecraft > Creating the bot...")

        bot = mineflayer.createBot(
            {
                "host": ServerConfig.host,
                "port": ServerConfig.port,
                "version": "1.8.9",
                "username": AccountConfig.email,
                "auth": "microsoft",
                "viewDistance": "tiny",
            }
        )

        print("Minecraft > Initialized")

        botcls = cls(client, bot)
        client.mineflayer_bot = botcls

        botcls._starting = True

        try:
            botcls.oncommands()
        except Exception as e:
            if "Call to 'on' timed out" in str(e):
                print(f"Minecraft > Error: {e}")
                print("Minecraft > Restarting...")
                botcls.stop()
                return cls.createbot(client)
            raise

        print("Minecraft > Events registered")

        botcls._starting = False

        return botcls
