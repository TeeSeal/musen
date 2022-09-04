from __future__ import annotations

from enum import IntEnum
from typing import TYPE_CHECKING

from commands.base_command import BaseCommand
from commands.checks import track_playing, user_is_in_same_voice_channel
from discord.app_commands import check, guild_only

if TYPE_CHECKING:
    from custom_types import ConnectedVoiceInteraction
    from lavalink import DefaultPlayer


class LoopSetting(IntEnum):
    off = 0
    track = 1
    queue = 2


class Loop(BaseCommand):
    description = "Loop tracks or queue"

    @guild_only
    @check(user_is_in_same_voice_channel)
    @check(track_playing)
    async def callback(
        self, interaction: ConnectedVoiceInteraction, type: LoopSetting
    ) -> None:
        player: DefaultPlayer = interaction.client.lavalink.player_manager.get(
            interaction.guild_id
        )

        player.set_loop(type)

        return await interaction.response.send_message(
            f"Set looping type to: `{type.name}`"
        )
