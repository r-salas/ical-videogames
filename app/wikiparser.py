#
#
#   Wiki games
#
#

import bs4
import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import Iterable, Iterator

from .data import Game, GameReleaseDate, Platform
from .utils import safe_strptime, replace_short_month


WIKI_BY_PLATFORM = {
    Platform.PC: "https://en.wikipedia.org/wiki/List_of_PC_games_(A)",
    Platform.PS5: "https://en.wikipedia.org/wiki/List_of_PlayStation_5_games",
    Platform.PS4: "https://en.wikipedia.org/wiki/List_of_PlayStation_4_games_(A–L)",
    Platform.NINTENDO_SWITCH: "https://en.wikipedia.org/wiki/List_of_Nintendo_Switch_games_(0–A)",
    Platform.NINTENDO_SWITCH_2: "https://en.wikipedia.org/wiki/List_of_Nintendo_Switch_2_games",
    Platform.XBOX_ONE: "https://en.wikipedia.org/wiki/List_of_Xbox_One_games_(A–L)",
    Platform.XBOX_SERIES: "https://en.wikipedia.org/wiki/List_of_Xbox_Series_X_and_Series_S_games",
}


def get_text(tag: bs4.element.Tag) -> str:
    return tag.get_text().strip()


def url_to_soup(url: str) -> BeautifulSoup:
    res = requests.get(url)
    res.raise_for_status()

    return BeautifulSoup(res.text, features="html.parser")


def iterate_wiki_rows(soup: BeautifulSoup) -> Iterator[bs4.element.Tag]:
    table = soup.select_one("table.wikitable.sortable")
    table_rows = table.find("tbody").find_all("tr")
    table_content_rows = table_rows[2:]  # Skip header rows

    for row in table_content_rows:
        yield row


def wiki_row_to_game(row: bs4.element.Tag, platform: Platform) -> Game:
    columns = row.select("tr > *")

    if platform in (Platform.NINTENDO_SWITCH, Platform.NINTENDO_SWITCH_2):
        date = safe_strptime(replace_short_month(get_text(columns[3])), '%B %d, %Y', date=True)
        jp_date, na_date, pal_date = [date] * 3
        title = get_text(columns[0])
        genre = None
        developer = get_text(columns[1])
        publisher = get_text(columns[2])
    if platform == Platform.PC:
        date = safe_strptime(replace_short_month(get_text(columns[5])), '%B %d, %Y', date=True)
        jp_date, na_date, pal_date = [date] * 3
        title = get_text(columns[0])
        developer = get_text(columns[1])
        publisher = get_text(columns[2])
        genre = get_text(columns[3])
    else:
        jp_date = safe_strptime(replace_short_month(get_text(columns[4])), '%B %d, %Y', date=True)
        na_date = safe_strptime(replace_short_month(get_text(columns[5])), '%B %d, %Y', date=True)
        pal_date = safe_strptime(replace_short_month(get_text(columns[6])), '%B %d, %Y', date=True)
        title = get_text(columns[0])
        genre = get_text(columns[1])
        developer = get_text(columns[2])
        publisher = get_text(columns[3])

    return Game(
        title=title,
        genre=genre,
        developer=developer,
        publisher=publisher,
        platform=platform,
        release_date=GameReleaseDate(
            jp=jp_date,
            na=na_date,
            pal=pal_date
        )
    )


def iterate_games(platforms: Iterable[Platform]):
    if not platforms:
        platforms = list(Platform)

    platforms = set(platforms)

    for platform in platforms:
        main_wiki_url = WIKI_BY_PLATFORM[platform]

        main_wiki_soup = url_to_soup(main_wiki_url)

        platform_games = set()

        for row in iterate_wiki_rows(main_wiki_soup):
            game = wiki_row_to_game(row, platform)
            platform_games.add(game)

        toc = main_wiki_soup.find(id="toc")

        if toc is not None:
            other_wikis = [link["href"] for link in toc.find_all("a", href=True) if not link["href"].startswith("#")]

            for wiki_path in other_wikis:
                full_url = urljoin(main_wiki_url, wiki_path)

                soup = url_to_soup(full_url)

                for row in iterate_wiki_rows(soup):
                    game = wiki_row_to_game(row, platform)
                    platform_games.add(game)

        for game in platform_games:
            yield game
