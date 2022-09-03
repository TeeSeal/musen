import os

import discord
from client import Client
from commands import commands

intents = discord.Intents.default()
client = Client(intents)
token = os.getenv("TOKEN")

for command in commands:
    client.register_command(command)

if token is not None:
    client.run(token)
