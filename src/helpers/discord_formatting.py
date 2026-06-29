from __future__ import annotations

import re
from typing import Any

import discord

emoji_regex = re.compile(r"<a?:(\w+):\d+>")
mention_regex = re.compile(r"<@!?(\d+)>")
role_mention_regex = re.compile(r"<@&(\d+)>")
channel_mention_regex = re.compile(r"<#(\d+)>")
slash_mention_regex = re.compile(r"</([\w\- ]+):\d+>")
link_regex = re.compile(r"(\S+)(\.+)(\S+)")


def _emoji_repl(match: re.Match[str]) -> str:
    return f":{match.group(1)}:"


def _slash_mention_repl(match: re.Match[str]) -> str:
    return f"/{match.group(1)}"


async def replace_discord_formatting(
    self: discord.Client,
    content: str,
    message: discord.Message,
) -> str:
    content = emoji_regex.sub(_emoji_repl, content)

    for mention in message.mentions:
        content = content.replace(f"<@!{mention.id}>", f"@{mention.name}")
        content = content.replace(f"<@{mention.id}>", f"@{mention.name}")

    for mentioned_role in message.role_mentions:
        content = content.replace(
            f"<@&{mentioned_role.id}>", f"@{mentioned_role.name}")

    for mentioned_channel in message.channel_mentions:
        content = content.replace(f"<#{mentioned_channel.id}>", f"#{
                                  mentioned_channel.name}")

    content = slash_mention_regex.sub(_slash_mention_repl, content)

    for mention in set(mention_regex.findall(content)):
        try:
            user = await self.fetch_user(int(mention))
            replacement = f"@{user.name}"
        except discord.NotFound:
            replacement = "@unknown-user"

        content = content.replace(f"<@!{mention}>", replacement)
        content = content.replace(f"<@{mention}>", replacement)

    guild = message.guild
    for mention in set(role_mention_regex.findall(content)):
        fetched_role = guild.get_role(
            int(mention)) if guild is not None else None
        replacement = f"@{fetched_role.name}" if fetched_role else "@unknown-role"
        content = content.replace(f"<@&{mention}>", replacement)

    for mention in set(channel_mention_regex.findall(content)):
        fetched_channel = self.get_channel(int(mention))
        channel_name = getattr(fetched_channel, "name", None)
        replacement = f"#{
            channel_name}" if channel_name else "#unknown-channel"
        content = content.replace(f"<#{mention}>", replacement)

    def _filter(match: re.Match[str]) -> str:
        thing = match.group(0)

        if not match.group(1).strip(".") or not match.group(3).strip("."):
            return thing

        tld = match.group(3)[:-1]
        if not tld:
            return thing

        try:
            int(tld)
        except ValueError:
            return "<link>"

        return thing

    return link_regex.sub(_filter, content)
