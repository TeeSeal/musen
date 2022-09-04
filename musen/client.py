from __future__ import annotations

import logging
import os
from typing import TYPE_CHECKING

import discord

from musen import voice
from musen.commands import commands
from musen.commands.tree import MusenCommandTree

if TYPE_CHECKING:
    from typing import Any


class MusenClient(discord.Client):
    def __init__(self) -> None:
        intents = discord.Intents()
        intents.guilds = True
        intents.voice_states = True

        super().__init__(intents=intents)

        self.tree = MusenCommandTree(self)
        self.register_commands()

    async def setup_hook(self) -> None:
        guild_id = os.getenv("TEST_GUILD_ID")

        if guild_id:
            guild = discord.Object(id=guild_id)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
        else:
            await self.tree.sync()

        if not hasattr(self, "lavalink"):
            self.lavalink = voice.LavalinkClient(self)

    def run(self, *args: Any, **kwargs: Any) -> None:
        discord.utils.setup_logging()
        token = os.getenv("TOKEN")

        if token is None:
            logging.critical("Could not find TOKEN in environment")
            exit(1)

        return super().run(token, log_handler=None)

    def register_commands(self) -> None:
        for cls in commands:
            command = cls()
            self.tree.command(
                name=command.name,
                description=command.description,
                nsfw=command.nsfw,
                guild=command.guild,
                guilds=command.guilds,
                auto_locale_strings=command.auto_locale_strings,
                extras=command.extras,
            )(command.callback)
