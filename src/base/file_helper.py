import os
from typing import TextIO

from src.base.base import root_dir


def move_file(src: str, dst: str) -> bool:
    try:
        if os.path.isfile(path):
            os.remove(path)
            return True
        else:
            raise Exception(f'not a file, path is: {path}')
    except NameError:
        print(NameError)
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
        file: TextIO = None,
        path: str = None
) -> list[str]:
    if (file is None and path is None) or (file is not None and path is not None):
        raise Exception('you should pass one and only one parameter')

    l: list[str] = []
    if file is None and path is not None:
        _file = open(path, mode='r', encoding='utf-8')
        for word in [line.rstrip() for line in _file.readlines()]:
            l.append(word)
    else:
        for word in [line.rstrip() for line in file.readlines()]:
            l.append(word)
    return l


def write_txt_file(path: str, data: str) -> bool:
    print(path)

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


if __name__ == '__main__':
    folder_path = root_dir(child='/files/cache/splitter')

    all_path = get_all_path_with_prefix(
        folder_path=folder_path,
        prefix='_'
    )

    print(all_path)
