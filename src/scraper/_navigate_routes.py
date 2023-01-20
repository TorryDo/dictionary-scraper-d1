from src.scraper.ConfigData import ConfigData, ConfigKeys
from src.scraper.ScrapeSource import ScrapeSources
from src.scraper._setup_props_and_create_workspace import _setup_props_and_create_workspace
from src.scraper.scraper_props import ScraperProps
from src.utils.FileHelper import FileHelper


def _navigate_routes(
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
