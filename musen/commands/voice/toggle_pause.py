from __future__ import annotations

from typing import TYPE_CHECKING

from commands.base_command import BaseCommand
from commands.checks import track_playing, user_is_in_same_voice_channel
from discord.app_commands import check, guild_only

if TYPE_CHECKING:
    from custom_types import ConnectedVoiceInteraction
    from lavalink import DefaultPlayer


class TogglePause(BaseCommand):
    description = "Toggle playback pause"

    @guild_only
    @check(user_is_in_same_voice_channel)
    @check(track_playing)
    async def callback(self, interaction: ConnectedVoiceInteraction) -> None:
        player: DefaultPlayer = interaction.client.lavalink.player_manager.get(
            interaction.guild_id
        )

        response = "Resumed" if player.paused else "Paused"
        await player.set_pause(not player.paused)
        return await interaction.response.send_message(response)
