from typing import Callable

from src.scraper.wiktionary.scrape_wiktionary import get_wiktionary_word_url


class ScrapeSource:
    id: int
    name: str
    get_word: Callable[[str], str]

    def __init__(self, id: int, name: str, get_word: Callable[[str], str]):
        self.id = id
        self.name = name
        self.get_word = get_word


class ScrapeSources:
    wiktionary_api = ScrapeSource(
        id=1,
        name='wiktionary api',
        get_word=get_wiktionary_word_url
    )
    other = ScrapeSource(
        id=2,
        name='other',
        get_word=get_wiktionary_word_url
    )

    @staticmethod
    def from_id(id: int)->ScrapeSource:
        if id == ScrapeSources.wiktionary_api.id:
            return ScrapeSources.wiktionary_api

        raise Exception(f"id = {id} not a valid id")
