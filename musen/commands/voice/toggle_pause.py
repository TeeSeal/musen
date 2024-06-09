from __future__ import annotations

from typing import TYPE_CHECKING

from discord.app_commands import check, guild_only

from musen.commands.base_command import BaseCommand
from musen.commands.checks import track_playing, user_is_in_same_voice_channel

if TYPE_CHECKING:
    from lavalink import DefaultPlayer

    from musen.custom_types import ConnectedVoiceInteraction


class TogglePause(BaseCommand):
    description = "Toggle playback pause"

    @guild_only
    @check(user_is_in_same_voice_channel)
    @check(track_playing)
    async def callback(self, interaction: ConnectedVoiceInteraction) -> None:  # type: ignore[override]
        player: DefaultPlayer = interaction.client.lavalink.player_manager.get(
            interaction.guild_id,
        )

        response = "Resumed" if player.paused else "Paused"
        await player.set_pause(not player.paused)
        return await interaction.response.send_message(response)
