import warnings

from bs4 import MarkupResemblesLocatorWarning
from tqdm import tqdm

from src.scraper.ConfigData import ConfigData, ConfigKeys
from src.scraper.ScrapeSource import ScrapeSource, ScrapeSources
from src.scraper._json2db import _json2db
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


def show_statistics():
    print('Statistics -------------------------')
    _total_words = ConfigData.get().get(ConfigKeys.word_number)
    _scraped_words = ConfigData.get().get(ConfigKeys.scrape_word_number)
    _scrape_source = ScrapeSources.from_id(ConfigData.get().get(ConfigKeys.scrape_source_id))
    _workspace_dir = ScraperProps.workspace_dir

    print(f"- total words: {_total_words}")
    print(f"- scraped words: {_scraped_words}")
    print(f"- error words: {_total_words - _scraped_words}")
    print(f"- scrape source: {_scrape_source.name}")
    print(f"- workspace dir: {_workspace_dir}")


def create_db_file():
    print('Creating .db file ...')

    _result_words_filepath = ScraperProps.result_success_jsontxt_filepath

    _json2db(
        table_name='EnglishVocabs',
        vocab_jsons=[js.removesuffix(',') for js in FileHelper.lines(_result_words_filepath)],
        dst=ScraperProps.result_dir + '/EnglishVocabs.db'
    )

    print('Success')

def create_excel_file():
    print('working on creating excel file')


def on_finished():
    print('mission success, the data have been collected in workspace dir.')
    while True:
        print('-------------------------')
        print('do you want to do any thing else?')

        print('1, show statistics')
        print('2, create .db file')
        print('3, create excel file (not yet)')
        print("99, delete workspace (can't undo)")

        print('your choice (enter to exit): ', end='')

        choice = input().replace(' ', '')
        if not choice.isdigit():
            break

        choice = int(choice)
        if choice == 1:
            show_statistics()
        if choice == 2:
            create_db_file()
        if choice == 3:
            create_excel_file()
        if choice == 99:
            if confirm_delete_workspace():
                exit()


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


def confirm_delete_workspace() -> bool:
    print('Do you want to abort this mission? (Y/n): ', end='')
    abort_char = input()
    if abort_char == 'Y':
        delete_workspace()
        print('workspace deleted, thank you for using me')
        return True
    return False


def delete_workspace():
    FileHelper.remove_dirs(ScraperProps.workspace_dir)
    FileHelper.delete_file(ScraperProps.workspace_filepath)


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
