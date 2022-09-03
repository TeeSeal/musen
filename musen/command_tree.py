from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from commands.errors import MusenCommandError
from discord import app_commands

if TYPE_CHECKING:
    from discord import Interaction

_log = logging.getLogger(__name__)


class MusenCommandTree(app_commands.CommandTree):
    async def on_error(
        self, interaction: Interaction, error: app_commands.AppCommandError, /
    ) -> None:
        if isinstance(error, MusenCommandError):
            if isinstance(interaction.command, app_commands.Command):
                command_name = interaction.command.name
                user = interaction.user
                err = error.__class__.__name__
                _log.info(
                    f"{user.name}({user.id}) failed to run `{command_name}`: {err}"
                )

            return await error.handle(interaction)

        return await super().on_error(interaction, error)
