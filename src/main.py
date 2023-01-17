from tqdm import tqdm

from src.scraper.manage_scraper import manage_scraper
from src.scraper.properties import ConfigData, ConfigKeys
from src.utils.FileHelper import FileHelper

_progress = tqdm(desc='Scraping', unit='word')
_current_word: int


def on_start():
    print('main on start')
    total_word_number = ConfigData.get().get(ConfigKeys.word_number)

    global _current_word
    _current_word = ConfigData.get().get(ConfigKeys.scrape_word_number)
    _progress.total = total_word_number
    _progress.update(_current_word)
    print(f'total_word_number = {total_word_number}')
    print(f'current_word_number = {_current_word}')


# if single word scraped, this function is called
def in_progress(**kwargs):
    global _current_word
    scraped_word_number = kwargs.get('scraped_word_number')
    if scraped_word_number is not None and scraped_word_number > 0:
        ConfigData.get()[ConfigKeys.scrape_word_number] += scraped_word_number
        ConfigData.save()
        return
    _current_word += 1
    _progress.update(_current_word)


def on_finished():
    pass


if __name__ == '__main__':
    manage_scraper(
        word_filepath=FileHelper.current_dir('../raw/words_alpha.txt'),
        workspace_directory=FileHelper.current_dir('../workspace'),
        on_start=on_start,
        in_progress=in_progress,
        on_finished=on_finished
    )
