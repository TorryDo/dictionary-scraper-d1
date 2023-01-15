from src.scraper.properties import ScraperProps, ConfigKeys
from src.scraper.setup_workspace import _setup_workspace
from src.scraper.split_word_file import split_to_smaller_word_file
from src.utils.FileHelper import FileHelper
from src.utils.JsonHelper import JsonHelper


def manage_scraper(
        word_filepath: str,
        workspace_directory: str = FileHelper.current_dir('../workspace'),
        scraper_number: int = 5,
        in_progress=None,
        on_finished=None,
):
    if not FileHelper.is_existed(word_filepath):
        raise Exception(f'file: {word_filepath} not existed')

    ScraperProps.in_progress = in_progress
    ScraperProps.on_finished = on_finished

    ScraperProps.scraper_number = scraper_number
    ScraperProps.word_filepath = word_filepath

    _setup_workspace(workspace_dir=workspace_directory)

    # all paths have been set

    def on_first_run(config_data: dict):
        print('on first run')
        cock = split_to_smaller_word_file(
            word_filepath=ScraperProps.word_filepath,
            dst_dir=ScraperProps.split_words_dir,
            rmdir_if_exists=True
        )
        config_data[ConfigKeys.word_number] = cock[ConfigKeys.word_number]
        FileHelper.write_text_file(
            path=ScraperProps.word_filepath,
            data=JsonHelper.dict2json(config_data)
        )

    def on_conflict_word_file() -> bool:
        print('on conflict word file')
        return True

    def on_resume(config_data: dict):
        print('on resume')
        remained_word_files: list[str] = list(filter(
            lambda f: f.startswith(ScraperProps.split_filename_prefix),
            FileHelper.children(from_root=ScraperProps.split_words_dir)
        ))
        if len(remained_word_files) == 0:
            finalize()
            return
        #     scraping...
        run_scrapers(
            number=ScraperProps.scraper_number,
            on_word_scraped=None
        )

    def finalize():
        print('finalize....')

    def on_finished(config_data: dict):
        print('on finished')
        ScraperProps.on_finished()

    navigate_routes_from_config_data(
        on_first_run=on_first_run,

        on_resume=on_resume,
        on_finished=on_finished,
        on_conflict_word_file=on_conflict_word_file,
    )


def run_scrapers(
        number: int,
        on_word_scraped,
):
    pass


def navigate_routes_from_config_data(
        on_first_run,
        on_resume,
        on_finished,
        on_conflict_word_file,
):
    datastr = FileHelper.read_file(ScraperProps.config_filepath)
    # on_first_run
    if datastr is None or len(datastr) == 0:
        config_data = dict()
        config_data['word_file_path'] = ScraperProps.word_filepath

        on_first_run(config_data)

        FileHelper.write_text_file(
            path=ScraperProps.config_filepath,
            data=JsonHelper.dict2json(config_data)
        )
        return

    config_data = JsonHelper.str2dict(datastr)
    if config_data.get(ConfigKeys.word_file_path) != ScraperProps.word_filepath:
        if on_conflict_word_file():
            return
        # on_resume / on_finished
    if config_data.get(ConfigKeys.result) is None:
        on_resume(config_data)
    else:
        on_finished(config_data)
