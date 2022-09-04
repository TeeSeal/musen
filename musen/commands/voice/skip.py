from __future__ import annotations

from typing import TYPE_CHECKING

from discord.app_commands import check, guild_only

from musen.commands.base_command import BaseCommand
from musen.commands.checks import track_playing, user_is_in_same_voice_channel
from musen.utils import format_track

if TYPE_CHECKING:
    from lavalink import DefaultPlayer

    from musen.custom_types import ConnectedVoiceInteraction


class Skip(BaseCommand):
    description = "Skip currently playing track"

    @guild_only
    @check(user_is_in_same_voice_channel)
    @check(track_playing)
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
