from typing import Optional

from src.utils.FileHelper import FileHelper
from src.utils.JsonHelper import JsonHelper


class ScraperProps:
    scraper_number: int
    word_filepath: str
    workspace_dir: str
    config_filepath: str
    result_dir: str
    error_words_dir: str
    success_words_dir: str

    wip_dir: str
    extract_words_dir: str
    split_words_dir: str
    scrape_queue_dir: str

    on_start = None
    in_progress = None
    on_finished = None

    split_filename_prefix = '_'


class ConfigKeys:
    word_file_path = 'word_file_path'
    word_number = 'word_number'
    in_progress = 'in_progress'
    total_split_file_number = 'total_split_file_number'
    scrape_word_number = 'scrape_word_number'
    result = 'result'
    success_word_number = 'success_word_number'
    error_word_number = 'error_word_number'


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
        if len(ConfigData._data) == 0:
            return False
        return True


"""
config.txt structure:
{
    word_file_path: string,
    word_number: int,
    in_progress: {
        // current_split_file_number: int,
        scrape_word_number: int
        total_split_file_number: int
    },
    result: {
        success_word_number: int,
        error_word_number: int
    }   
}
"""
