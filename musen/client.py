from __future__ import annotations

import os
from typing import TYPE_CHECKING

import discord
from commands.tree import MusenCommandTree
from voice import lavalink

if TYPE_CHECKING:
    from typing import Type

    from commands.base_command import BaseCommand


class MusenClient(discord.Client):
    def __init__(self, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = MusenCommandTree(self)

    async def setup_hook(self) -> None:
        guild_id = os.getenv("TEST_GUILD_ID")

        if guild_id:
            guild = discord.Object(id=guild_id)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
        else:
            await self.tree.sync()

    async def on_connect(self) -> None:
        if not hasattr(self, "lavalink"):
            self.lavalink = lavalink.Client(self)

    def register_command(self, cls: Type[BaseCommand]) -> None:
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
