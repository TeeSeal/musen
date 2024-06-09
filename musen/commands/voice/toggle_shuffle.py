from __future__ import annotations

from typing import TYPE_CHECKING

from discord.app_commands import check, guild_only

from musen.commands.base_command import BaseCommand
from musen.commands.checks import track_playing, user_is_in_same_voice_channel

if TYPE_CHECKING:
    from lavalink import DefaultPlayer

    from musen.custom_types import ConnectedVoiceInteraction


class ToggleShuffle(BaseCommand):
    description = "Toggle queue shuffling"

    @guild_only
    @check(user_is_in_same_voice_channel)
    @check(track_playing)
    async def callback(self, interaction: ConnectedVoiceInteraction) -> None:  # type: ignore[override]
        player: DefaultPlayer = interaction.client.lavalink.player_manager.get(
            interaction.guild_id,
        )

        response = (
            "Stopped shuffling queue" if player.shuffle else "Now shuffling queue"
        )
        player.set_shuffle(not player.shuffle)
        return await interaction.response.send_message(response)
