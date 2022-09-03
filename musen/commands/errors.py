from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from discord.app_commands import AppCommandError

if TYPE_CHECKING:
    from discord import Interaction


class MusenCommandError(AppCommandError, ABC):
    @abstractmethod
    async def handle(self, interaction: Interaction) -> None:
        ...


class UserNotInVoiceChannel(MusenCommandError):
    async def handle(self, interaction: Interaction) -> None:
        await interaction.response.send_message("You must be in a voice channel")


class BotNotInVoiceChannel(MusenCommandError):
    async def handle(self, interaction: Interaction) -> None:
        await interaction.response.send_message("Not connected")


class UserNotInCurrentVoiceChannel(MusenCommandError):
    async def handle(self, interaction: Interaction) -> None:
        await interaction.response.send_message("We must be in the same voice channel")
