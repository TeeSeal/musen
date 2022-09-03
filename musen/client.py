from typing import Type

import discord
from commands.base_command import BaseCommand
from discord import app_commands

MY_GUILD = discord.Object(id=117271426867789833)


class Client(discord.Client):
    def __init__(self, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

    # async def on_ready(self) -> None:
    #     self.tree.clear_commands(guild=MY_GUILD)
    #     self.tree.clear_commands(guild=None)
    #     await self.tree.sync()

    def register_command(self, command: BaseCommand) -> None:
        self.tree.command(
            name=command.name,
            description=command.description,
            nsfw=command.nsfw,
            guild=command.guild,
            guilds=command.guilds,
            auto_locale_strings=command.auto_locale_strings,
            extras=command.extras,
        )(command.handler)