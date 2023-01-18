import warnings
from enum import Enum

from bs4 import MarkupResemblesLocatorWarning
from tqdm import tqdm

from src.scraper.ConfigData import ConfigData, ConfigKeys
from src.scraper.manage_scraper import manage_scraper
from src.utils.FileHelper import FileHelper

_progress: tqdm
_current_scraped_word_number: int


def on_start():
    print('start scraping ...')
    total_word_number = ConfigData.get().get(ConfigKeys.word_number)

    global _current_scraped_word_number
    _current_scraped_word_number = ConfigData.get().get(ConfigKeys.scrape_word_number)

    print(f'total_word_number = {total_word_number}')
    print(f'current_word_number = {_current_scraped_word_number}')

    global _progress
    _progress = tqdm(
        desc='Scraping',
        unit='word',
        initial=_current_scraped_word_number,
        total=total_word_number
    )


# if single word scraped, this function is called
def in_progress(**kwargs):
    global _current_scraped_word_number
    scraped_word_number = kwargs.get('scraped_word_number_in_file')
    if scraped_word_number is not None and scraped_word_number > 0:
        ConfigData.get()[ConfigKeys.scrape_word_number] += scraped_word_number
        ConfigData.save()
        return
    _current_scraped_word_number += 1
    _progress.n = _current_scraped_word_number
    _progress.refresh()


def on_finished():
    pass


class ScrapeSource(Enum):
    WiktionaryApi = 'wiktionary api'
    Others = 'others'


def choose_scrape_source() -> ScrapeSource:
    print('Choose one source to start scraping:')
    options = [
        ScrapeSource.WiktionaryApi,
        ScrapeSource.Others
    ]

    for i in range(len(options)):
        print(f'{i + 1}, {options[i].value}')

    print('Your choice is: ', end='')
    position = int(input())

    return options[position - 1]


def display_previous_data():
    print('Previous data:')
    scraping_source = ScrapeSource.WiktionaryApi
    print(f'1, Scraping source: {scraping_source.value}')
    total_word = 370_000
    print(f'- Total words: {total_word}')
    scraped_word = 10_000
    print(f'- Scraped words: {scraped_word}')


def on_init():
    pass


if __name__ == '__main__':
    display_previous_data()
    warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning, module='bs4')
    manage_scraper(
        word_filepath=FileHelper.current_dir('../raw/words_alpha.txt'),
        workspace_directory=FileHelper.current_dir('../workspace'),
        on_start=on_start,
        in_progress=in_progress,
        on_finished=on_finished,
        scraper_number=60
    )
