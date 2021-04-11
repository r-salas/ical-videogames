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
    PS5 = "ps5"
    PS4 = "ps4"
    NINTENDO_SWITCH = "switch"
    XBOX_ONE = "xbox_one"
    XBOX_SERIES = "xbox_series"


@dataclass
class GameReleaseDate:

    jp: Optional[datetime.datetime]   # Japan
    na: Optional[datetime.datetime]   # North America
    pal: Optional[datetime.datetime]  # Europe and Australasia


@dataclass
class Game:

    title: str
    genre: str
    developer: str
    publisher: str
    platform: Platform
    release_date: GameReleaseDate
