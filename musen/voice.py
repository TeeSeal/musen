from __future__ import annotations

import os
from typing import TYPE_CHECKING, cast

import discord
import lavalink
from lavalink import DefaultPlayer

if TYPE_CHECKING:
    from discord.types.voice import GuildVoiceState, VoiceServerUpdate

    from musen.client import MusenClient


class DiscordClientNotConnected(Exception):
    pass


class LavalinkEventHooks:
    def __init__(
        self, musen_client: MusenClient, lavalink_client: LavalinkClient
    ) -> None:
        self.musen = musen_client
        self.lavalink = lavalink_client

    @lavalink.listener(lavalink.events.QueueEndEvent)
    async def on_queue_end(self, event: lavalink.events.QueueEndEvent) -> None:
        guild_id = event.player.guild_id
        guild = self.musen.get_guild(guild_id)

        if guild and guild.voice_client:
            await guild.voice_client.disconnect(force=True)


class LavalinkClient(lavalink.Client):
    def __init__(self, musen_client: MusenClient):
        self.musen = musen_client

        if not musen_client.user:
            raise DiscordClientNotConnected

        super().__init__(musen_client.user.id)

        self.add_node(
            host=os.getenv("LAVALINK_HOST", "localhost"),
            port=int(os.getenv("LAVALINK_PORT", "2333")),
            password=os.getenv("LAVALINK_PASSWORD", "2333"),
            region=os.getenv("LAVALINK_REGION", "eu"),
        )

        event_hooks = LavalinkEventHooks(self.musen, self)
        self.add_event_hooks(event_hooks)


class LavalinkVoiceClient(discord.VoiceClient):
    def __init__(
        self, client: MusenClient, channel: discord.voice_client.VocalGuildChannel
    ):
        super().__init__(client, channel)
        self.client = client
        self.channel_id = channel.id
        self.lavalink = self.client.lavalink

    async def on_voice_server_update(self, data: VoiceServerUpdate) -> None:
        lavalink_data = {"t": "VOICE_SERVER_UPDATE", "d": data}
        await self.lavalink.voice_update_handler(lavalink_data)

    async def on_voice_state_update(self, data: GuildVoiceState) -> None:
        self.set_channel_id(data)
        lavalink_data = {"t": "VOICE_STATE_UPDATE", "d": data}
        await self.lavalink.voice_update_handler(lavalink_data)

    async def connect(
        self,
        *,
        timeout: float,
        reconnect: bool,
        self_deaf: bool = False,
        self_mute: bool = False,
    ) -> None:
        self.lavalink.player_manager.create(guild_id=self.channel.guild.id)
        await self.channel.guild.change_voice_state(
            channel=self.channel, self_mute=self_mute, self_deaf=self_deaf
        )

    async def disconnect(self, *, force: bool = False) -> None:
        player = cast(
            DefaultPlayer, self.lavalink.player_manager.get(self.channel.guild.id)
        )

        if not force and not player.is_connected:
            return

        await self.channel.guild.change_voice_state(channel=None)

        player.channel_id = None
        self.cleanup()

    def set_channel_id(self, data: GuildVoiceState) -> None:
        if "member" not in data or not self.client or not self.client.user:
            return

        if int(data["member"]["user"]["id"]) == self.client.user.id:
            self.channel_id = int(data["channel_id"])
