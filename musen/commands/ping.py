from .base_command import BaseCommand, Interaction


class Ping(BaseCommand):
    description = "Pong!"

    async def handler(self, interaction: Interaction) -> None:
        await interaction.response.send_message("Pong!")
