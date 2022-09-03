from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from discord.utils import MISSING
from utils import to_camel

if TYPE_CHECKING:
    from typing import Any, Optional, Sequence, Union

    from discord import Interaction
    from discord.abc import Snowflake
    from discord.app_commands.translator import locale_str


class BaseCommand(ABC):
    description: Union[str, locale_str] = MISSING
    nsfw: bool = False
    guild: Optional[Snowflake] = MISSING
    guilds: Sequence[Snowflake] = MISSING
    auto_locale_strings: bool = True
    extras: dict[Any, Any] = MISSING

    @property
    def name(self) -> Union[str, locale_str]:
        return to_camel(self.__class__.__name__)

    @abstractmethod
    async def handler(self, interaction: Interaction) -> None:
        ...
