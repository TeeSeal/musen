from __future__ import annotations

import re
from typing import TYPE_CHECKING

from commands.base_command import BaseCommand
from commands.checks import user_is_in_voice_channel
from discord.app_commands import check, guild_only
from voice.lavalink_voice_client import LavalinkVoiceClient

if TYPE_CHECKING:
    from custom_types import VoiceInteraction

url_rx = re.compile(r"https?://(?:www\.)?.+")


class Play(BaseCommand):
    description = "Search and play a track or playlist for the given query"

    @guild_only
    @check(user_is_in_voice_channel)
    async def callback(self, interaction: VoiceInteraction, query: str) -> None:
        player = interaction.client.lavalink.player_manager.create(interaction.guild_id)
        query = query.strip("<>")

        if not url_rx.match(query):
            query = f"ytsearch:{query}"

        results = await player.node.get_tracks(query)

        if not results or not results.tracks:
            return await interaction.response.send_message("Found nothing")

        player.store("channel", interaction.channel_id)
        await interaction.user.voice.channel.connect(cls=LavalinkVoiceClient)  # type: ignore

        if results.load_type == "PLAYLIST_LOADED":
            tracks = results.tracks

            for track in tracks:
                player.add(requester=interaction.user.id, track=track)

            response = f"Playlist enqueued\n{results.playlist_info.name} - {len(tracks)} tracks"
        else:
            track = results.tracks[0]
            player.add(requester=interaction.user.id, track=track)
            response = f"Track enqueued\n[{track.title}]({track.uri})"

        await interaction.response.send_message(response)

        if not player.is_playing:
            await player.play()
