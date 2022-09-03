from .base_command import BaseCommand
from .ping import Ping

commands: list[BaseCommand] = [Ping()]
