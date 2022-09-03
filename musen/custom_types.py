from client import MusenClient
from discord import Interaction as OriginalInteraction


class Interaction(OriginalInteraction):
    client: MusenClient
