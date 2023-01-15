from src.scraper.properties import ConfigKeys
from src.utils.FileHelper import FileHelper


def split_to_smaller_word_file(
        word_filepath: str,
        dst_dir: str,
        each_word_per_file: int = 200,
        prefix_each_file: str = '_',
        rmdir_if_exists=False
) -> dict:
    cock = dict()
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

    cock[ConfigKeys.word_number] = len(word_list)
    return cock
