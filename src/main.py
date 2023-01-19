import warnings

from bs4 import MarkupResemblesLocatorWarning
from tqdm import tqdm

from src.scraper.ConfigData import ConfigData, ConfigKeys
from src.scraper.ScrapeSource import ScrapeSource, ScrapeSources
from src.scraper.manage_scraper import manage_scraper
from src.scraper.scraper_props import ScraperProps
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


def choose_scrape_source() -> ScrapeSource:
    print('Choose one source to start scraping:')
    options = [
        ScrapeSources.wiktionary_api,
        ScrapeSources.other
    ]

    for i in range(len(options)):
        print(f'{i + 1}, {options[i].name}')

    print('Your choice is: ', end='')
    position = int(input())

    return options[position - 1] if position in range(len(options)) else exit()


# call to user input config properties
def on_init_user_choose_config_properties() -> dict:
    cock = dict()

    print('Hi, Before scraping please let me know some informations:')
    print('- word file path (.txt): ', end='')
    word_filepath = input()

    print('- workspace directory (enter to choose current dir): ', end='')
    workspace_dir = input()
    if workspace_dir is None or workspace_dir == '':
        workspace_dir = FileHelper.current_dir('../workspace2')

    print(f'workspace dir = {workspace_dir}')
    scrape_source = choose_scrape_source()

    cock[ConfigKeys.word_file_path] = word_filepath
    cock[ConfigKeys.workspace_dir] = workspace_dir
    cock[ConfigKeys.scrape_source_id] = scrape_source.id
    return cock


def delete_workspace():
    print('delete workspace not finished')
    pass


def on_confirm_information() -> dict:
    cock = dict()
    scraper_number = 30
    if ScraperProps.scraper_number is not None:
        scraper_number = ScraperProps.scraper_number

    scrape_source = ScraperProps.scrape_source

    print("ok, I collected some information from you, these shouldn't be changed from now (unless cancel task)")
    print(f"- word file path: {ScraperProps.word_filepath}")
    print(f"- workspace dir: {ScraperProps.workspace_dir}")
    print(f"- scrape source: {scrape_source.name}")
    print('please confirm these information:')
    print(f'1, scraper number = {scraper_number}')
    print(f'2, cancel current task')
    print('Type number to choose/change (enter to skip): ', end='')
    choice = input()
    if choice == 1 or choice == '1':
        print('please select scraper number (require > 0): ', end='')
        scraper_number = int(input())
    elif choice == 2 or choice == '2':
        print('Do you want to abort this mission? (Y/n): ')
        abort_char = input()
        if abort_char == 'Y':
            delete_workspace()
            print('data deleted, thank you for using me')
            exit()

    cock[ConfigKeys.scraper_number] = scraper_number
    return cock


if __name__ == '__main__':
    warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning, module='bs4')
    manage_scraper(
        on_init_choose_config_properties=on_init_user_choose_config_properties,
        on_confirm_information=on_confirm_information,
        on_start_scraping=on_start,
        in_progress=in_progress,
        on_finished=on_finished,
    )
#     word_filepath=FileHelper.current_dir('../raw/words_alpha.txt'),
#         workspace_directory=FileHelper.current_dir('../workspace'),
