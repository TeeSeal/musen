from __future__ import annotations

from typing import TYPE_CHECKING, cast
from urllib.parse import urlencode

from discord import ClientUser

from musen.commands.base_command import BaseCommand

if TYPE_CHECKING:
    from musen.custom_types import MusenInteraction


class Invite(BaseCommand):
    description = "Get my invitation URL"

    async def callback(self, interaction: MusenInteraction) -> None:  # type: ignore[override]
        user = cast(ClientUser, interaction.client.user)
        params = {"client_id": user.id, "scope": "bot", "permissions": 36700160}
        url = "https://discord.com/api/oauth2/authorize?" + urlencode(params)
        await interaction.response.send_message(url)
