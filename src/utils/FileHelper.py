import os.path
from pathlib import Path


class FileHelper:

    @staticmethod
    def mkdir(path: str):
        # abspath = FileHelper.current_dir(path)
        # Path(abspath).mkdir(parents=parents, exist_ok=exist_ok)
        os.mkdir(path)

    @staticmethod
    def rmdir(path: str):
        # abspath = FileHelper.current_dir(path)
        # Path(abspath).rmdir()
        os.rmdir(path)

    @staticmethod
    def current_dir(child: str = None) -> str:
        result: str = ''

        result += os.path.abspath(os.curdir).replace('\\', '/')

        if child is not None:
            dot2slash = '../'
            while child.startswith(dot2slash):
                last_slash_pos = result.rfind('/')
                result = result[:last_slash_pos]
                child = child.removeprefix(dot2slash)
            result += '/' + child

        return result

    @staticmethod
    def is_file(path: str) -> bool:
        return os.path.isfile(path)

    @staticmethod
    def is_dir(path: str) -> bool:
        return os.path.isdir(path)

    @staticmethod
    def is_existed(path: str) -> bool:
        return os.path.exists(path)

    @staticmethod
    def children(dir_path: str = None) -> list[str]:
        path = FileHelper.current_dir(dir_path)
        if not os.path.exists(path):
            raise Exception(f'Path "{path}" not exists')

        return os.listdir(path)

    @staticmethod
    def create_file(path: str, encoding='utf-8'):
        f = open(path, mode='x', encoding=encoding)
        f.close()
        print(f.errors)

    @staticmethod
    def write_text_file(path: str, data: str, encoding='utf-8') -> bool:
        try:
            file = open(path, mode='w', encoding=encoding)
            file.write(data)
            file.close()
            return True
        except NameError:
            return False

    @staticmethod
    def read_file(path: str, encoding='utf-8') -> str:
        file = open(path, mode='r', encoding=encoding)
        result = file.read()
        file.close()
        return result

    @staticmethod
    def split_each_line(path: str) -> list[str]:
        l: list[str] = []
        _file = open(path, mode='r', encoding='utf-8')
        text = _file.readlines()
        for word in [line.rstrip() for line in text]:
            l.append(word)

        _file.close()
        return l

    @staticmethod
    def delete_file(path: str):
        if os.path.isfile(path):
            os.remove(path)
        else:
            raise Exception(f'not a file, path is: {path}')


if __name__ == '__main__':
    curidr = FileHelper.current_dir()
    print(curidr)
