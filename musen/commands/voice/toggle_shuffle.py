from __future__ import annotations

from typing import TYPE_CHECKING

from commands.base_command import BaseCommand
from commands.checks import track_playing, user_is_in_same_voice_channel
from discord.app_commands import check, guild_only

if TYPE_CHECKING:
    from custom_types import ConnectedVoiceInteraction
    from lavalink import DefaultPlayer


class ToggleShuffle(BaseCommand):
    description = "Toggle queue shuffling"

    @guild_only
    @check(user_is_in_same_voice_channel)
    @check(track_playing)
    async def callback(self, interaction: ConnectedVoiceInteraction) -> None:
        player: DefaultPlayer = interaction.client.lavalink.player_manager.get(
            interaction.guild_id
        )

        response = (
            "Stopped shuffling queue" if player.shuffle else "Now shuffling queue"
        )
        player.set_shuffle(not player.shuffle)
        return await interaction.response.send_message(response)
