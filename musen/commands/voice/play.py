from __future__ import annotations

import re
from typing import TYPE_CHECKING

from discord.app_commands import check, describe, guild_only

from musen.commands.base_command import BaseCommand
from musen.commands.checks import user_is_in_voice_channel
from musen.utils import format_track
from musen.voice import LavalinkVoiceClient

if TYPE_CHECKING:
    from lavalink import DefaultPlayer

    from musen.custom_types import VoiceInteraction


url_rx = re.compile(r"https?://(?:www\.)?.+")


class Play(BaseCommand):
    description = "Search and play a track or playlist for the given query"

    @guild_only
    @check(user_is_in_voice_channel)
    @describe(query="URL or search query")
    async def callback(self, interaction: VoiceInteraction, query: str) -> None:
        player: DefaultPlayer = interaction.client.lavalink.player_manager.create(
            interaction.guild_id
        )
        query = query.strip("<>")

        if not url_rx.match(query):
            query = f"ytsearch:{query}"

        results = await player.node.get_tracks(query)

        if not results or not results.tracks:
            return await interaction.response.send_message("Found nothing")

        if results.load_type == "PLAYLIST_LOADED":
            tracks = results.tracks

            for track in tracks:
                player.add(requester=interaction.user.id, track=track)

            response = f"Playlist enqueued\n{results.playlist_info.name} - {len(tracks)} tracks"
        else:
            track = results.tracks[0]
            player.add(requester=interaction.user.id, track=track)
            formatted = format_track(track, prefix="")
            response = f"Track enqueued\n{formatted}"

        await interaction.response.send_message(response)

        if not player.is_connected:
            player.store("channel", interaction.channel_id)
            await interaction.user.voice.channel.connect(cls=LavalinkVoiceClient)  # type: ignore

        if not player.is_playing:
            await player.play()
