import asyncio
import re
import shutil
from typing import Callable, Optional

from src.model.vocab.vocab import Vocab
from src.scraper.ConfigData import ConfigData, ConfigKeys
from src.scraper.ScrapeSource import ScrapeSources
from src.scraper.ScrapeState import ScrapeState
from src.scraper.move_files_from_queue_to_split import move_files_from_queue_to_split
from src.scraper.scraper_props import ScraperProps
from src.scraper.setup_workspace import _setup_props_and_create_workspace
from src.scraper.split_word_file import split_to_smaller_word_file
from src.scraper.wiktionary.scrape_wiktionary import scrape_wiktionary_word
from src.utils.FileHelper import FileHelper


def _default_confirm_information() -> dict:
    return {
        ConfigKeys.scrape_source_id: ScrapeSources.wiktionary_api,
        ConfigKeys.scraper_number: 20,
    }


_on_confirm_information: Optional[Callable] = None
_on_init_choose_config_properties: Optional[Callable] = None


def manage_scraper(
        on_init_choose_config_properties: Callable[[], dict],
        on_confirm_information: Callable[[], dict] = _default_confirm_information,
        on_start_scraping=None,
        in_progress=None,
        on_finished=None,
):
    global _on_confirm_information
    global _on_init_choose_config_properties
    _on_confirm_information = on_confirm_information
    _on_init_choose_config_properties = on_init_choose_config_properties

    ScraperProps.on_start_scraping = on_start_scraping
    ScraperProps.in_progress = in_progress
    ScraperProps.on_finished = on_finished

    # all properties have been set
    navigate_routes_from_config_data(
        on_first_run=_on_first_run,
        on_resume=_on_resume,
        on_finished=_on_finished,
    )


# lifecycles #################################################################

def _on_first_run():
    print('_on first run')

    cock = _on_init_choose_config_properties()
    temp_word_filepath = cock[ConfigKeys.word_file_path].replace('\\', '/')
    temp_workspace_dir = cock[ConfigKeys.workspace_dir].replace('\\', '/')
    temp_scrape_src_id = cock[ConfigKeys.scrape_source_id]
    if not FileHelper.is_existed(temp_word_filepath):
        raise Exception(f'file: {temp_word_filepath} not existed')

    ScraperProps.word_filepath = temp_word_filepath
    ScraperProps.scrape_source = ScrapeSources.from_id(temp_scrape_src_id)
    _setup_props_and_create_workspace(temp_workspace_dir)

    ConfigData.set({})

    ConfigData.get()[ConfigKeys.word_file_path] = temp_word_filepath
    ConfigData.get()[ConfigKeys.workspace_dir] = temp_workspace_dir
    ConfigData.get()[ConfigKeys.scrape_source_id] = temp_scrape_src_id
    ConfigData.get()[ConfigKeys.scrape_word_number] = 0

    cock = split_to_smaller_word_file(
        word_filepath=ScraperProps.word_filepath,
        dst_dir=ScraperProps.split_words_dir,
    )

    ConfigData.get()[ConfigKeys.word_number] = cock[ConfigKeys.word_number]
    ConfigData.save()

    ScraperProps.workspace_filepath = FileHelper.current_dir('../workspace.txt')
    data = temp_workspace_dir
    FileHelper.write_text_file(
        path=ScraperProps.workspace_filepath,
        data=data
    )

    _on_resume()


def _on_conflict_word_file() -> bool:
    print('on conflict word file')
    return True


def _on_resume():
    print('on resume')
    cock_confirm = _on_confirm_information()
    scraper_number = cock_confirm[ConfigKeys.scraper_number]
    if scraper_number <= 0:
        raise Exception('required scraper number > 0')
    print(f'scraper number on resume = {scraper_number}')
    ScraperProps.scraper_number = scraper_number

    move_files_from_queue_to_split()

    remained_word_files: list[str] = list(filter(
        lambda f: f.startswith(ScraperProps.split_filename_prefix),
        FileHelper.children(from_root=ScraperProps.split_words_dir)
    ))
    if len(remained_word_files) == 0:
        _finalize()
        return
    #     scraping...

    ScraperProps.on_start_scraping()

    asyncio.run(run_scrapers(number=ScraperProps.scraper_number))

    ConfigData.get()[ConfigKeys.state] = ScrapeState.Scraped.value
    ConfigData.save()
    _finalize()


# wip
def _finalize():
    print('finalizing...')

    def sort_filename_by_number_from_dir(
            src_dir
    ) -> list[str]:
        names = [name for name in FileHelper.children(from_root=src_dir)]
        names.sort(key=lambda f: int(re.sub('\D', '', f)))
        return [src_dir + '/' + name for name in names]

    # save success words txt
    success_word_paths = sort_filename_by_number_from_dir(ScraperProps.success_words_dir)
    success_word_datatxt = ',\n'.join([FileHelper.read_file(path) for path in success_word_paths])
    FileHelper.write_text_file(
        path=ScraperProps.result_success_jsontxt_filepath,
        data=success_word_datatxt
    )

    # save error words txt
    error_word_paths = sort_filename_by_number_from_dir(ScraperProps.error_words_dir)
    error_words_datatxt = '\n'.join([FileHelper.read_file(path) for path in error_word_paths])
    FileHelper.write_text_file(
        path=ScraperProps.result_error_txt_filepath,
        data=error_words_datatxt
    )

    # save state and call on_finished
    ConfigData.get()[ConfigKeys.state] = ScrapeState.Finalized.value
    ConfigData.save()

    _on_finished()


def _on_finished():
    print('on finished')
    ScraperProps.on_finished()


# end of lifecycle #################################################################

_word_filename: list[str] = []


async def run_scrapers(
        number: int,
):
    global _word_filename

    _word_filename = FileHelper.children(from_root=ScraperProps.split_words_dir)

    tasks = list()
    for _ in range(number):
        tasks.append(asyncio.create_task(
            _scrape_words_then_move_file(
                src_dir=ScraperProps.split_words_dir,
                queue_dir=ScraperProps.scrape_queue_dir,
                dst_dir=ScraperProps.success_words_dir,
                error_dir=ScraperProps.error_words_dir,
            )
        ))

    await asyncio.wait(tasks)


async def _scrape_words_then_move_file(
        src_dir,
        queue_dir,
        dst_dir,
        error_dir
):
    while len(_word_filename) > 0:
        filename = _word_filename.pop(0)
        src = src_dir + '/' + filename
        dst = queue_dir + '/' + filename

        shutil.move(src=src, dst=dst)

        words = FileHelper.lines(dst)

        vocabs: list[Vocab] = []
        error_words: list[str] = []
        for word in words:
            vocab = await scrape_wiktionary_word(word)
            if vocab is not None:
                vocabs.append(vocab)
                if ScraperProps.in_progress is not None:
                    ScraperProps.in_progress()
            else:
                error_words.append(word)

        data = ',\n'.join(map(lambda x: x.toJson(), vocabs))
        FileHelper.write_text_file(
            path=dst_dir + f'/{filename}',
            data=data
        )

        if len(error_words) > 0:
            error_data = '\n'.join(error_words)
            FileHelper.write_text_file(
                path=error_dir + f'/{filename}',
                data=error_data
            )

        FileHelper.delete_file(path=dst)

        if ScraperProps.in_progress is not None:
            ScraperProps.in_progress(scraped_word_number_in_file=len(vocabs))


def navigate_routes_from_config_data(
        on_first_run,
        on_resume,
        on_finished,
):
    ScraperProps.workspace_filepath = FileHelper.current_dir('../workspace.txt')
    if not FileHelper.is_existed(ScraperProps.workspace_filepath):
        on_first_run()
        return

    # initialized
    ScraperProps.workspace_dir = FileHelper.read_file(ScraperProps.workspace_filepath)
    _setup_props_and_create_workspace(ScraperProps.workspace_dir)

    if ConfigData.is_finalized():
        on_finished()
        return

    ScraperProps.word_filepath = ConfigData.get().get(ConfigKeys.word_file_path)
    ScraperProps.scrape_source = ScrapeSources.from_id(ConfigData.get().get(ConfigKeys.scrape_source_id))
    on_resume()
