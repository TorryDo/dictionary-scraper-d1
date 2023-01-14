import time

from src.utils.FileHelper import FileHelper
from src.utils.JsonHelper import JsonHelper


def _word_url(word: str) -> str:
    base_url = "https://en.wiktionary.org/api/rest_v1/page/definition"
    return base_url + '/' + word


_scraper_number: int

_word_filepath: str
_workspace_dir: str

_config_filepath: str
config_data = dict()

_result_dir: str
_error_words_dir: str
_success_words_dir: str

_wip_dir: str
_extract_words_dir: str
_split_words_dir: str

"""
config.txt structure:
{
    word_file_path: string,
    word_number: int,
    in_progress: {
        current_split_file_number: int,
        total_split_file_number: int
    },
    result: {
        scraped_word_number: int,
        error_word_number: int
    }   
}
"""


def _setup_workspace(workspace_dir: str):
    global _workspace_dir
    global _config_filepath
    _workspace_dir = workspace_dir
    _config_filepath = _workspace_dir + '/config.txt'

    if not FileHelper.is_existed(workspace_dir):
        FileHelper.make_dirs(workspace_dir)

    if not FileHelper.is_existed(_config_filepath):
        FileHelper.create_file(_config_filepath)

    global _result_dir
    global _error_words_dir
    global _success_words_dir
    _result_dir = workspace_dir + '/result'
    _error_words_dir = _result_dir + '/error_words'
    _success_words_dir = _result_dir + '/success_words'

    global _wip_dir
    global _extract_words_dir
    global _split_words_dir
    _wip_dir = workspace_dir + '/wip'
    _extract_words_dir = _wip_dir + '/extract_words'
    _split_words_dir = _wip_dir + '/split_words'

    FileHelper.make_dirs(_result_dir)
    FileHelper.make_dirs(_error_words_dir)
    FileHelper.make_dirs(_success_words_dir)

    FileHelper.make_dirs(_wip_dir)
    FileHelper.make_dirs(_extract_words_dir)
    FileHelper.make_dirs(_split_words_dir)


def _init_config_file():
    config_data['word_file_path'] = _word_filepath


def scrape_wiktionary(
        word_filepath: str,
        workspace_directory: str = FileHelper.current_dir('../workspace'),
        scraper_number: int = 5,
        in_progress=None,
        on_finished=None,
):
    if not FileHelper.is_existed(word_filepath):
        raise Exception(f'file: {word_filepath} not existed')

    global _scraper_number
    _scraper_number = scraper_number
    global _word_filepath
    _word_filepath = word_filepath

    _setup_workspace(workspace_dir=workspace_directory)

    # global config_data
    # config_data = FileHelper.read_file(_config_filepath)
    # if config_data is None or len(config_data) == 0:
    #     _init_config_file()
    # data: dict = JsonHelper.str2dict()


def split_to_smaller_word_file(
        word_filepath: str,
        dst_dir: str,
        each_word_per_file: int = 200,
        prefix_each_file: str = '_',
        rmdir_if_exists=False
):
    word_list: list[str] = FileHelper.split_each_line(word_filepath)
    count = 0

    if FileHelper.is_existed(dst_dir):
        if rmdir_if_exists:
            FileHelper.remove_dirs(dst_dir)
        elif len(FileHelper.children(from_root=dst_dir)) > 0:
            raise Exception(f"destination dir:{dst_dir} is not empty")

    FileHelper.make_dirs(dst_dir)

    while count < len(word_list):
        temp_list: list[str]

        if len(word_list) >= each_word_per_file:
            temp_list = word_list[count:(count + each_word_per_file)]
            count += each_word_per_file
        else:
            temp_list = word_list
            count = len(word_list)

        if len(temp_list) == 0:
            break

        data = ''
        for word in temp_list:
            data += f'{word}\n'

        split_filepath = dst_dir + f'/{prefix_each_file}{count}.txt'
        FileHelper.write_text_file(path=split_filepath, data=data)


if __name__ == '__main__':
    split_to_smaller_word_file(
        word_filepath=FileHelper.current_dir('../raw/words_alpha.txt'),
        dst_dir=FileHelper.current_dir('../raw/testt'),
        rmdir_if_exists=True
    )
