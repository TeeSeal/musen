from __future__ import annotations

from typing import TYPE_CHECKING

from commands.base_command import BaseCommand
from commands.checks import user_is_in_same_voice_channel
from discord.app_commands import check, guild_only
from utils import format_track

if TYPE_CHECKING:
    from custom_types import ConnectedVoiceInteraction
    from lavalink import DefaultPlayer


class Skip(BaseCommand):
    description = "Skip currently playing track"

    @guild_only
    @check(user_is_in_same_voice_channel)
    async def callback(self, interaction: ConnectedVoiceInteraction) -> None:
        player: DefaultPlayer = interaction.client.lavalink.player_manager.get(
            interaction.guild_id
        )

        track = player.current
        await player.skip()

        response = "Skipped"
        if track:
            response += " " + format_track(track, prefix="")

        return await interaction.response.send_message(response)
