from __future__ import annotations

from typing import TYPE_CHECKING

from .util.ping import Ping
from .voice.play import Play
from .voice.stop import Stop

if TYPE_CHECKING:
    from .base_command import BaseCommand

commands: list[BaseCommand] = [Ping(), Play(), Stop()]
