from __future__ import annotations

import os
from typing import TYPE_CHECKING

import discord
import lavalink
from commands.tree import MusenCommandTree

if TYPE_CHECKING:
    from commands.base_command import BaseCommand

MY_GUILD = discord.Object(id=117271426867789833)


class MusenClient(discord.Client):
    def __init__(self, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = MusenCommandTree(self)

    async def setup_hook(self) -> None:
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

    # async def on_ready(self) -> None:
    #     self.tree.clear_commands(guild=MY_GUILD)
    #     self.tree.clear_commands(guild=None)
    #     await self.tree.sync()

    async def on_connect(self) -> None:
        if self.user is not None:
            self.lavalink = lavalink.Client(self.user.id)
            self.lavalink.add_node(
                host=os.getenv("LAVALINK_HOST", "localhost"),
                port=os.getenv("LAVALINK_PORT", 2333),
                password=os.getenv("LAVALINK_PASSWORD", 2333),
                region=os.getenv("LAVALINK_REGION", "eu"),
            )

    def register_command(self, command: BaseCommand) -> None:
        self.tree.command(
            name=command.name,
            description=command.description,
            nsfw=command.nsfw,
            guild=command.guild,
            guilds=command.guilds,
            auto_locale_strings=command.auto_locale_strings,
            extras=command.extras,
        )(command.callback)
