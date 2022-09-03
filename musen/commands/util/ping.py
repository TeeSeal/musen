from __future__ import annotations

from typing import TYPE_CHECKING

from commands.base_command import BaseCommand

if TYPE_CHECKING:
    from discord import Interaction


class Ping(BaseCommand):
    description = "Pong!"

    async def handler(self, interaction: Interaction) -> None:
        await interaction.response.send_message("Pong!")
