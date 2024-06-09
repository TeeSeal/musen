from __future__ import annotations

from typing import TYPE_CHECKING

from discord import Guild, Interaction, Member, VoiceClient, VoiceState

if TYPE_CHECKING:
    from typing import Union

    from discord.channel import StageChannel, VoiceChannel

    from musen.client import MusenClient

    VocalGuildChannel = Union[VoiceChannel, StageChannel]


class MusenInteraction(Interaction):
    client: MusenClient


class GuildInteraction(MusenInteraction):
    guild: Guild
    user: Member


class VoiceStateWithChannel(VoiceState):
    channel: VocalGuildChannel


class MemberInVoiceChannel(Member):
    voice: VoiceStateWithChannel


class VoiceInteraction(GuildInteraction):
    user: MemberInVoiceChannel


class VoiceClientWithChannel(VoiceClient):
    channel: VocalGuildChannel


class GuildWithVoiceClient(Guild):
    voice_client: VoiceClientWithChannel


class ConnectedVoiceInteraction(VoiceInteraction):
    guild: GuildWithVoiceClient
