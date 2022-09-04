import logging
import os

import discord

from musen.client import MusenClient
from musen.commands import commands

discord.utils.setup_logging()

intents = discord.Intents()
intents.guilds = True
intents.voice_states = True

client = MusenClient(intents)

for command in commands:
    client.register_command(command)

token = os.getenv("TOKEN")

if token is None:
    logging.critical("Could not find TOKEN in environment")
    exit(1)

client.run(token, log_handler=None)