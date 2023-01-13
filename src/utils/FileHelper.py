import os.path


class FileHelper:

    @staticmethod
    def current_dir(child: str = None) -> str:
        result = ''

        result += os.path.abspath(os.curdir).replace('\\', '/')

        if child is not None:
            result += child

        return result

    @staticmethod
    def is_file(path: str) -> bool:
        return os.path.isfile(path)

    @staticmethod
    def is_dir(path: str) -> bool:
        pass

    @staticmethod
    def is_existed(path: str) -> bool:
        return os.path.exists(path)

    @staticmethod
    def children(dir_path: str) -> list[str]:
        if not os.path.exists(dir_path):
            raise Exception(f'Path "{dir_path}" not exists')

        return os.listdir(dir_path)

    @staticmethod
    def is_empty_directory():
        pass

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
            return True
        except NameError:
            return False

    @staticmethod
    def split_each_line(path: str) -> list[str]:
        l: list[str] = []
        _file = open(path, mode='r', encoding='utf-8')
        text = _file.readlines()
        for word in [line.rstrip() for line in text]:
            l.append(word)
        return l

    @staticmethod
    def delete_file(path: str):
        if os.path.isfile(path):
            os.remove(path)
        else:
            raise Exception(f'not a file, path is: {path}')


if __name__ == '__main__':
    paths = FileHelper.split_each_line(FileHelper.current_dir('/raw/test_words.txt'))
    print(paths)
