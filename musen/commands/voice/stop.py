from __future__ import annotations

from typing import TYPE_CHECKING

from commands.base_command import BaseCommand
from commands.checks import user_is_in_same_voice_channel
from discord.app_commands import check, guild_only

if TYPE_CHECKING:
    from custom_types import ConnectedVoiceInteraction


class Stop(BaseCommand):
    description = "Search and play a track for the given query"

    @guild_only
    @check(user_is_in_same_voice_channel)
    async def callback(self, interaction: ConnectedVoiceInteraction) -> None:
        player = interaction.client.lavalink.player_manager.get(interaction.guild_id)

        player.queue.clear()
        await player.stop()

        await interaction.guild.voice_client.disconnect(force=True)
        return await interaction.response.send_message("Disconnected")
