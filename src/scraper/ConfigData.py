from typing import Optional

from src.scraper.ScrapeState import ScrapeState
from src.scraper.scraper_props import ScraperProps
from src.utils.FileHelper import FileHelper
from src.utils.JsonHelper import JsonHelper


class ConfigKeys:
    state = 'state'
    word_file_path = 'word_file_path'
    scrape_source_id = 'scrape_source_id'
    scraper_number = 'scraper_number'
    workspace_dir = 'workspace_dir'
    word_number = 'word_number'
    total_split_file_number = 'total_split_file_number'
    scrape_word_number = 'scrape_word_number'


class ConfigData:
    _data: Optional[dict] = None

    @staticmethod
    def set(data: dict):
        ConfigData._data = data

    @staticmethod
    def save(path: str = None):
        if path is None:
            path = ScraperProps.config_filepath
        FileHelper.write_text_file(
            path=path,
            data=JsonHelper.dict2json(ConfigData._data)
        )

    @staticmethod
    def update_from_file(path=None) -> dict:
        if path is None:
            path = ScraperProps.config_filepath
        if path is None or path == '':
            raise Exception(f'path = {path} not valid')

        datastr = FileHelper.read_file(path)
        if datastr is None or datastr == '':
            ConfigData._data = {}
            ConfigData.save()
            return ConfigData._data
        ConfigData._data = JsonHelper.str2dict(datastr)
        return ConfigData._data

    @staticmethod
    def get(path=None) -> dict:
        if path is None:
            path = ScraperProps.config_filepath

        return ConfigData._data \
            if ConfigData._data is not None \
            else ConfigData.update_from_file()

    @staticmethod
    def is_initialized() -> bool:
        try:
            ConfigData.update_from_file()
        except:
            return False

        if len(ConfigData._data) == 0:
            return False
        return True

    @staticmethod
    def is_finalized() -> bool:
        conf_state = ConfigData.get().get(ConfigKeys.state)
        if conf_state is None:
            return False
        if conf_state == ScrapeState.Finalized.value:
            return True

        return False


"""
config.txt structure:
{
    word_file_path: string,
    word_number: int,
    // current_split_file_number: int,
    scrape_word_number: int,
    total_split_file_number: int,

    success_word_number: int,
    error_word_number: int,
}
"""
