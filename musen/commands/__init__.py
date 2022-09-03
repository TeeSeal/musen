from .base_command import BaseCommand
from .util.ping import Ping

commands: list[BaseCommand] = [Ping()]
