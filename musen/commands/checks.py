from typing import cast

from discord import Interaction
from lavalink import DefaultPlayer

from musen.commands.errors import (
    BotNotInVoiceChannelError,
    UserNotInCurrentVoiceChannelError,
    UserNotInVoiceChannelError,
)
from musen.custom_types import ConnectedVoiceInteraction, GuildInteraction
from musen.voice import LavalinkVoiceClient


async def user_is_in_voice_channel(interaction: Interaction) -> bool:
    interaction = cast(GuildInteraction, interaction)

    if interaction.user.voice and interaction.user.voice.channel:
        return True

    raise UserNotInVoiceChannelError


async def bot_is_in_voice_channel(interaction: Interaction) -> bool:
    interaction = cast(GuildInteraction, interaction)

    if interaction.guild.voice_client and interaction.guild.voice_client.channel:
        return True

    raise BotNotInVoiceChannelError


async def user_is_in_same_voice_channel(interaction: Interaction) -> bool:
    await bot_is_in_voice_channel(interaction)

    try:
        await user_is_in_voice_channel(interaction)
    except UserNotInVoiceChannelError as err:
        raise UserNotInCurrentVoiceChannelError from err

    interaction = cast(ConnectedVoiceInteraction, interaction)
    voice_client = cast(LavalinkVoiceClient, interaction.guild.voice_client)

    if interaction.user.voice.channel.id == voice_client.channel_id:
        return True

    raise UserNotInCurrentVoiceChannelError


async def track_playing(interaction: Interaction) -> bool:
    interaction = cast(GuildInteraction, interaction)

    player = cast(
        DefaultPlayer,
        interaction.client.lavalink.player_manager.get(interaction.guild.id),
    )

    return player.is_playing
