from src.scraper.properties import ScraperProps
from src.utils.FileHelper import FileHelper


def _setup_workspace(workspace_dir: str):
    ScraperProps.workspace_dir = workspace_dir
    ScraperProps.config_filepath = ScraperProps.workspace_dir + '/config.txt'

    if not FileHelper.is_existed(workspace_dir):
        FileHelper.make_dirs(workspace_dir)

    if not FileHelper.is_existed(ScraperProps.config_filepath):
        FileHelper.create_file(ScraperProps.config_filepath)

    ScraperProps.result_dir = workspace_dir + '/result'
    ScraperProps.error_words_dir = ScraperProps.result_dir + '/error_words'
    ScraperProps.success_words_dir = ScraperProps.result_dir + '/success_words'

    ScraperProps.wip_dir = workspace_dir + '/wip'
    ScraperProps.extract_words_dir = ScraperProps.wip_dir + '/extract_words'
    ScraperProps.split_words_dir = ScraperProps.wip_dir + '/split_words'
    ScraperProps.scrape_queue_dir = ScraperProps.wip_dir + '/scrape_queue'

    FileHelper.make_dirs(ScraperProps.result_dir)
    FileHelper.make_dirs(ScraperProps.error_words_dir)
    FileHelper.make_dirs(ScraperProps.success_words_dir)

    FileHelper.make_dirs(ScraperProps.wip_dir)
    FileHelper.make_dirs(ScraperProps.extract_words_dir)
    FileHelper.make_dirs(ScraperProps.split_words_dir)
    FileHelper.make_dirs(ScraperProps.scrape_queue_dir)
