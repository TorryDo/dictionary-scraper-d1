import os.path
import shutil


class FileHelper:

    @staticmethod
    def make_dirs(path: str, exist_ok=True):
        os.makedirs(path, exist_ok=exist_ok)

    @staticmethod
    def remove_dirs(path: str):
        shutil.rmtree(path)

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
    def children(from_current: str = None, from_root: str = None) -> list[str]:
        path: str
        if from_root is not None:
            path = from_root
        else:
            path = FileHelper.current_dir(from_current)

        if not os.path.exists(path):
            raise Exception(f'Path "{path}" not exists')

        return os.listdir(path)

    @staticmethod
    def create_file(path: str, encoding='utf-8'):
        f = open(path, mode='x', encoding=encoding)
        f.close()

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
    def lines(path: str) -> list[str]:
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
