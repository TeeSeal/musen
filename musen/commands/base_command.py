from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Sequence, Union

from discord import Interaction
from discord.abc import Snowflake
from discord.app_commands.translator import locale_str
from discord.utils import MISSING
from utils import to_camel


class BaseCommand(ABC):
    description: Union[str, locale_str] = MISSING
    nsfw: bool = False
    guild: Optional[Snowflake] = MISSING
    guilds: Sequence[Snowflake] = MISSING
    auto_locale_strings: bool = True
    extras: Dict[Any, Any] = MISSING

    @property
    def name(self) -> Union[str, locale_str]:
        return to_camel(self.__class__.__name__)

    @abstractmethod
    async def handler(self, interaction: Interaction) -> None:
        ...
