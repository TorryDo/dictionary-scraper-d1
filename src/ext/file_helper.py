import os
from typing import TextIO

from src.base.base import root_dir


def is_empty_folder_exist(path: str) -> bool:
    if is_exist(path) and is_folder_empty(path):
        return True

    return False


def is_exist(path: str) -> bool:
    return os.path.exists(path)


def is_folder_empty(path: str) -> bool:
    # if not is_exist(path):
    #     return True
    file_paths = get_all_path(folder_path=path)

    if len(file_paths) == 0:
        return True

    return False


def remove_file(path: str) -> bool:
    try:
        if os.path.isfile(path):
            os.remove(path)
            return True
        else:
            raise Exception(f'not a file, path is: {path}')
    except NameError:
        print(NameError)
        return False


def create_dir_if_not_exists(dir_path: str) -> bool:
    try:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        return True
    except NameError:
        print(NameError)
        return False


def read_each_line(
        path: str = None,
        file: TextIO = None,
        remove_suffix=None,
        remove_prefix=None

) -> list[str]:
    if (file is None and path is None) or (file is not None and path is not None):
        raise Exception('you should pass one and only one parameter')

    l: list[str] = []
    if file is None and path is not None:
        _file = open(path, mode='r', encoding='utf-8')
        text = _file.readlines()
        # if remove_suffix is not None:
        #     text = remove_suffix(text)
        # if remove_prefix is not None:
        #     text = remove_prefix(text)
        for word in [line.rstrip() for line in text]:
            l.append(word)
    else:
        text = file.readlines()
        for word in [line.rstrip() for line in text]:
            l.append(word)
    return l


def write_txt_file(path: str, data: str) -> bool:
    try:
        file = open(path, mode='w', encoding='utf-8')
        file.write(data)
        return True
    except NameError:
        return False


def get_all_path_with_prefix(
        folder_path: str,
        prefix: str = '_'
) -> list[str]:
    if not os.path.exists(folder_path):
        # raise Exception('Path not exists')
        return []
    all_path = os.listdir(folder_path)
    l: list[str] = []
    for path in all_path:
        if path.startswith(prefix):
            l.append(path)

    return l


def get_all_path(
        folder_path: str,
) -> list[str]:
    if not os.path.exists(folder_path):
        # raise Exception('Path not exists')
        return []

    return os.listdir(folder_path)


if __name__ == '__main__':
    folder_path = root_dir(child='/files/cache/splitter')

    all_path = get_all_path_with_prefix(
        folder_path=folder_path,
        prefix='_'
    )

    print(all_path)
