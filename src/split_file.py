import os
import shutil

from src.base.base import root_dir
from src.base.file_helper import write_txt_file, read_each_line, get_all_path_with_prefix


def split_huge_text_file_to_multiple_smaller_file(
        source_path: str,
        cache_splitter_dir_path: str = root_dir(child='/files/cache/splitter'),
        each_word_per_file: int = 500,
        prefix_each_file: str = '_'
):
    is_already_split = is_file_already_split(
        config_path=f'{cache_splitter_dir_path}/config.txt',
        words_path=source_path
    )
    if is_already_split:
        print('this file is already split, return')
        return
    else:
        if os.path.exists(cache_splitter_dir_path):
            shutil.rmtree(cache_splitter_dir_path)

    word_list: list[str] = read_each_line(path=source_path)

    count = 0

    while count < len(word_list):

        temp_list: list[str]

        if len(word_list) >= each_word_per_file:
            temp_list = word_list[count:(count + each_word_per_file)]
            count += each_word_per_file
        else:
            temp_list = word_list
            count += len(word_list)

        if len(temp_list) == 0:
            break

        if not os.path.exists(cache_splitter_dir_path):
            os.makedirs(cache_splitter_dir_path)

        with open(cache_splitter_dir_path + f'/{prefix_each_file}{count}.txt', mode='w', encoding='utf-8') as f:
            temp = ''
            for word in temp_list:
                temp += f'{word}\n'
            f.write(temp)

    save_data_config = source_path + '\n'
    all_path = get_all_path_with_prefix(
        folder_path=root_dir(child='/files/cache/splitter'),
        prefix='_'
    )
    save_data_config += str(len(all_path)) + '\n'

    succeed = write_config_file(
        file_path=f'{cache_splitter_dir_path}/config.txt',
        data=save_data_config
    )

    if succeed:
        print('save split succeed')
    else:
        print('save error')


def write_config_file(
        file_path: str,
        data: str
) -> bool:
    try:
        folder_path = os.path.dirname(file_path)
        print(f'folder path: {folder_path}')
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        write_txt_file(
            path=file_path,
            data=data
        )

        return True
    except NameError:
        return False


def is_file_already_split(
        config_path: str,
        words_path: str
) -> bool:
    print(config_path)
    if not os.path.exists(config_path):
        return False

    is_file_existed: list[str] = read_each_line(path=config_path)
    if len(is_file_existed) == 0:
        return False
    else:
        if is_file_existed[0] == words_path:
            return True
        else:
            return False
