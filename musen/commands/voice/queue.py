from __future__ import annotations

from typing import TYPE_CHECKING

from commands.base_command import BaseCommand
from commands.checks import bot_is_in_voice_channel
from discord.app_commands import check, guild_only
from utils import format_track

if TYPE_CHECKING:
    from custom_types import ConnectedVoiceInteraction
    from lavalink import DefaultPlayer


class Queue(BaseCommand):
    description = "Show current track queue"

    @guild_only
    @check(bot_is_in_voice_channel)
    async def callback(self, interaction: ConnectedVoiceInteraction) -> None:
        player: DefaultPlayer = interaction.client.lavalink.player_manager.get(
            interaction.guild_id
        )

        response_lines = []

        if player.current:
            current_track = format_track(player.current, prefix="")
            response_lines.append(f"Now playing: {current_track}")

        response_lines.extend(("", "Queue:"))
        response_lines.extend(map(format_track, player.queue[:10]))

        queue_len = len(player.queue)
        if queue_len > 10:
            response_lines.append(f"\nAnd {queue_len - 10} more")

        response = "\n".join(response_lines)
        return await interaction.response.send_message(response)
