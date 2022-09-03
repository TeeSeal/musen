from __future__ import annotations

from typing import TYPE_CHECKING

from commands.base_command import BaseCommand

if TYPE_CHECKING:
    from custom_types import MusenInteraction


class Ping(BaseCommand):
    description = "Pong!"

    async def callback(self, interaction: MusenInteraction) -> None:
        await interaction.response.send_message("Pong!")
