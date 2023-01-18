import asyncio
import shutil

from src.model.vocab.vocab import Vocab
from src.scraper.move_files_from_queue_to_split import move_files_from_queue_to_split
from src.scraper.properties import ScraperProps, ConfigKeys, ConfigData
from src.scraper.setup_workspace import _setup_workspace
from src.scraper.split_word_file import split_to_smaller_word_file
from src.scraper.wiktionary.scrape_wiktionary import scrape_wiktionary_word
from src.utils.FileHelper import FileHelper


def manage_scraper(
        word_filepath: str,
        workspace_directory: str = FileHelper.current_dir('../workspace'),
        scraper_number: int = 5,
        on_start=None,
        in_progress=None,
        on_finished=None,
):
    if not FileHelper.is_existed(word_filepath):
        raise Exception(f'file: {word_filepath} not existed')

    if scraper_number == 0:
        raise Exception('required scraper number > 0')

    ScraperProps.on_start = on_start
    ScraperProps.in_progress = in_progress
    ScraperProps.on_finished = on_finished

    ScraperProps.scraper_number = scraper_number
    ScraperProps.word_filepath = word_filepath

    _setup_workspace(workspace_dir=workspace_directory)

    # all properties have been set
    navigate_routes_from_config_data(
        on_first_run=_on_first_run,
        on_resume=_on_resume,
        on_finished=_on_finished,
        on_conflict_word_file=_on_conflict_word_file,
    )


# lifecycles #################################################################

def _on_first_run():
    print('_on first run')
    cock = split_to_smaller_word_file(
        word_filepath=ScraperProps.word_filepath,
        dst_dir=ScraperProps.split_words_dir,
    )
    ConfigData.get()[ConfigKeys.word_number] = cock[ConfigKeys.word_number]
    ConfigData.save()

    _on_resume()


def _on_conflict_word_file() -> bool:
    print('on conflict word file')
    return True


def _on_resume():
    print('on resume')
    ScraperProps.on_start()
    remained_word_files: list[str] = list(filter(
        lambda f: f.startswith(ScraperProps.split_filename_prefix),
        FileHelper.children(from_root=ScraperProps.split_words_dir)
    ))
    if len(remained_word_files) == 0:
        _finalize()
        return
    #     scraping...

    move_files_from_queue_to_split()
    asyncio.run(run_scrapers(number=ScraperProps.scraper_number))

    _finalize()


# wip
def _finalize():
    print('finalizing...')
    # ConfigData.get()[ConfigKeys.result][ConfigKeys.]



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
        on_conflict_word_file,
):
    ConfigData.update_from_file()

    # on_first_run
    if not ConfigData.is_initialized():
        print('on is_initialized')
        ConfigData.get()[ConfigKeys.word_file_path] = ScraperProps.word_filepath
        ConfigData.get()[ConfigKeys.scrape_word_number] = 0
        ConfigData.save()
        on_first_run()
        return

    if ConfigData.get().get(ConfigKeys.word_file_path) != ScraperProps.word_filepath:
        if on_conflict_word_file():
            return
        # on_resume / on_finished
    if ConfigData.get().get(ConfigKeys.result) is None:
        on_resume()
    else:
        on_finished()
