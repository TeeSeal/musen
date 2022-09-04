from __future__ import annotations

from typing import TYPE_CHECKING

from .util.ping import Ping
from .voice.play import Play
from .voice.queue import Queue
from .voice.skip import Skip
from .voice.stop import Stop

if TYPE_CHECKING:
    from typing import Type

    from .base_command import BaseCommand

commands: list[Type[BaseCommand]] = [Ping, Play, Stop, Queue, Skip]
