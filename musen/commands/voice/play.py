from __future__ import annotations

import re
from typing import TYPE_CHECKING

from commands.base_command import BaseCommand
from discord import Member
from voice.lavalink_voice_client import LavalinkVoiceClient

if TYPE_CHECKING:
    from custom_types import Interaction

url_rx = re.compile(r"https?://(?:www\.)?.+")


class Play(BaseCommand):
    description = "Search and play a track for the given query"

    async def callback(self, interaction: Interaction, query: str) -> None:
        if not isinstance(interaction.user, Member) or not interaction.guild:
            return await interaction.response.send_message(
                "This command can only be used in a server"
            )

        user = interaction.user
        if not user.voice or not user.voice.channel:
            return await interaction.response.send_message("Join a voice channel first")

        player = interaction.client.lavalink.player_manager.create(interaction.guild_id)
        query = query.strip("<>")

        if not url_rx.match(query):
            query = f"ytsearch:{query}"

        results = await player.node.get_tracks(query)

        if not results or not results.tracks:
            return await interaction.response.send_message("Found nothing")

        player.store("channel", interaction.channel_id)
        await user.voice.channel.connect(cls=LavalinkVoiceClient)  # type: ignore

        if results.load_type == "PLAYLIST_LOADED":
            tracks = results.tracks

            for track in tracks:
                player.add(requester=interaction.user.id, track=track)

            response = f"Playlist Enqueued!\n{results.playlist_info.name} - {len(tracks)} tracks"
        else:
            track = results.tracks[0]
            player.add(requester=interaction.user.id, track=track)
            response = f"Track Enqueued\n[{track.title}]({track.uri})"

        await interaction.response.send_message(response)

        if not player.is_playing:
            await player.play()
