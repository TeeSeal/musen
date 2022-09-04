from __future__ import annotations

from typing import TYPE_CHECKING

from .util.invite import Invite
from .util.ping import Ping
from .voice.loop import Loop
from .voice.play import Play
from .voice.queue import Queue
from .voice.skip import Skip
from .voice.stop import Stop
from .voice.toggle_pause import TogglePause
from .voice.toggle_shuffle import ToggleShuffle

if TYPE_CHECKING:
    from typing import Type

    from .base_command import BaseCommand

commands: list[Type[BaseCommand]] = [
    Ping,
    Play,
    Stop,
    Queue,
    Skip,
    TogglePause,
    ToggleShuffle,
    Loop,
    Invite,
]
