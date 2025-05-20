#
#
#   Data
#
#

import datetime

from enum import Enum
from typing import Optional
from dataclasses import dataclass


class Platform(Enum):
    PC = "pc"
    PS5 = "ps5"
    PS4 = "ps4"
    NINTENDO_SWITCH = "switch"
    NINTENDO_SWITCH_2 = "switch_2"
    XBOX_ONE = "xbox_one"
    XBOX_SERIES = "xbox_series"


@dataclass(frozen=True, eq=True)
class GameReleaseDate:

    jp: Optional[datetime.date]   # Japan
    na: Optional[datetime.date]   # North America
    pal: Optional[datetime.date]  # Europe and Australasia


@dataclass(frozen=True, eq=True)
class Game:

    title: str
    genre: str
    developer: str
    publisher: str
    platform: Platform
    release_date: GameReleaseDate
