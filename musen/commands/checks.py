from typing import cast

from commands.errors import (
    BotNotInVoiceChannel,
    UserNotInCurrentVoiceChannel,
    UserNotInVoiceChannel,
)
from custom_types import ConnectedVoiceInteraction, GuildInteraction
from discord import Interaction


async def user_is_in_voice_channel(interaction: Interaction) -> bool:
    interaction = cast(GuildInteraction, interaction)

    if interaction.user.voice and interaction.user.voice.channel:
        return True

    raise UserNotInVoiceChannel


async def bot_is_in_voice_channel(interaction: Interaction) -> bool:
    interaction = cast(GuildInteraction, interaction)

    if interaction.guild.voice_client and interaction.guild.voice_client.channel:
        return True

    raise BotNotInVoiceChannel


async def user_is_in_same_voice_channel(interaction: Interaction) -> bool:
    await bot_is_in_voice_channel(interaction)

    try:
        await user_is_in_voice_channel(interaction)
    except UserNotInVoiceChannel:
        raise UserNotInCurrentVoiceChannel

    interaction = cast(ConnectedVoiceInteraction, interaction)

    if interaction.user.voice.channel.id == interaction.guild.voice_client.channel.id:
        return True

    raise UserNotInCurrentVoiceChannel
