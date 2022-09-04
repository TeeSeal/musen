from __future__ import annotations

from typing import TYPE_CHECKING, cast
from urllib.parse import urlencode

from commands.base_command import BaseCommand
from discord import ClientUser

if TYPE_CHECKING:
    from custom_types import MusenInteraction


class Invite(BaseCommand):
    description = "Get my invitation URL"

    async def callback(self, interaction: MusenInteraction) -> None:
        user = cast(ClientUser, interaction.client.user)
        params = {"client_id": user.id, "scope": "bot", "permissions": 36700160}
        url = "https://discord.com/api/oauth2/authorize?" + urlencode(params)
        await interaction.response.send_message(url)
