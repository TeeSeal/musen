from __future__ import annotations

from typing import TYPE_CHECKING

from musen.commands.base_command import BaseCommand

if TYPE_CHECKING:
    from musen.custom_types import MusenInteraction


class Ping(BaseCommand):
    description = "Pong!"

    async def callback(self, interaction: MusenInteraction) -> None:  # type: ignore[override]
        await interaction.response.send_message("Pong!")
