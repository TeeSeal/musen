from __future__ import annotations

from typing import TYPE_CHECKING

from commands.base_command import BaseCommand
from discord import Member

if TYPE_CHECKING:
    from custom_types import Interaction


class Stop(BaseCommand):
    description = "Search and play a track for the given query"

    async def callback(self, interaction: Interaction) -> None:
        if not isinstance(interaction.user, Member) or not interaction.guild:
            return await interaction.response.send_message(
                "This command can only be used in a server"
            )

        player = interaction.client.lavalink.player_manager.get(interaction.guild_id)

        if not interaction.guild.voice_client:
            return await interaction.response.send_message("Not connected")

        user: Member = interaction.user
        if (
            not user.voice
            or not user.voice.channel
            or (player.is_connected and user.voice.channel.id != int(player.channel_id))
        ):
            return await interaction.response.send_message("Not connected")

        player.queue.clear()
        await player.stop()

        await interaction.guild.voice_client.disconnect(force=True)
        return await interaction.response.send_message("Disconnected")
