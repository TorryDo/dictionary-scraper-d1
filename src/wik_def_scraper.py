# wiktionary definition scraper
import json
import os.path
import shutil

import requests
from bs4 import BeautifulSoup

from src.base.base import root_dir
from src.base.file_helper import (
    get_all_path_with_prefix,
    create_dir_if_not_exists,
    read_each_line,
    write_txt_file,
    remove_file
)
from src.model.vocab.vocab import Vocab
from src.model.vocab.word_type import WordType
from src.model.vocab.word_type_definition import WordTypeDefinition
from src.split_file import split_huge_text_file_to_multiple_smaller_file

base_def_url = "https://en.wiktionary.org/api/rest_v1/page/definition"
finished_words_file_path = "../files/cache/finished_words.txt"

check_words: list[str] = []
check_words_file = open(finished_words_file_path, mode='a+', encoding='utf-8')
check_words_file.seek(0)
check_words_list = [line.rstrip() for line in check_words_file.readlines()]

for word in check_words_list:
    check_words.append(word)

words_alpha_txt = root_dir('/raw/words_alpha.txt')

splitter_dir_path = root_dir(child='/files/cache/splitter')
config_file_path = splitter_dir_path + '/config.txt'
temp_splitter_dir_path = root_dir(child='/files/cache/temp_splitter')

temp_data_mine_dir_path = root_dir(child='/files/cache/temp_data_mine')
data_mine_dir_path = root_dir(child='/files/data_mine')


def run_scraper(
        words_file_path: str = words_alpha_txt,
        accept_empty_word: bool = True,
        threads: int = 2,
        progress=None
):
    split_huge_text_file_to_multiple_smaller_file(
        source_path=words_file_path,
        cache_splitter_dir_path=root_dir(child='/files/cache/splitter'),
        each_word_per_file=200,
        prefix_each_file='_'
    )

    previous_temp_file_words: list[str] = get_all_path_with_prefix(folder_path=temp_splitter_dir_path, prefix='_')
    if len(previous_temp_file_words) > 0:
        print('previous task still ongoing')
        return

    cache_word_file_names: list[str] = get_all_path_with_prefix(folder_path=splitter_dir_path, prefix='_')

    create_dir_if_not_exists(dir_path=temp_splitter_dir_path)

    # should put it in loop
    first_name = cache_word_file_names[0]
    cache_word_file_names.pop(0)

    src_temp_word_file_path = splitter_dir_path + '/' + first_name
    dst_temp_word_file_path = temp_splitter_dir_path + '/' + first_name
    temp_data_mine_file_path = temp_data_mine_dir_path + '/' + first_name

    scrape_word_then_move_file(
        src_path=src_temp_word_file_path,
        dst_path=dst_temp_word_file_path,
        temp_data_mine_path=temp_data_mine_file_path
    )


def scrape_with_threads(
        cache_dir_path: str = root_dir(child='/files/cache'),
        quantity: int = 2
): pass


def scrape_word_then_move_file(
        src_path: str,
        dst_path: str,
        temp_data_mine_path: str
) -> bool:
    try:

        shutil.move(src=src_path, dst=dst_path)

        vocab_list: list[Vocab] = scrape_words(
            words=read_each_line(path=dst_path),
            accept_empty_word=False
        )

        temp_rs = ''
        for vocab in vocab_list:
            temp_rs += vocab.toJson() + ',\n'
        temp_rs = temp_rs.removesuffix('\n')

        create_dir_if_not_exists(dir_path=temp_data_mine_dir_path)
        write_txt_file(path=temp_data_mine_path, data=temp_rs)

        remove_file(path=dst_path)

        return True
    except NameError:
        print(NameError)
        if os.path.exists(dst_path):
            shutil.move(src=dst_path, dst=src_path)
            print(f'moved dst: {dst_path} -to- src{src_path} due to exception')
        return False


def scrape_words(
        words: list[str],
        on_each_word=None,
        accept_empty_word: bool = True,
) -> list[Vocab]:
    #
    vocab_list: list[Vocab] = []

    for word in words:

        vocab = scrape_word(word)

        if accept_empty_word:
            vocab_list.append(vocab)
        else:
            if len(vocab.word_type) > 0:
                vocab_list.append(vocab)

        if on_each_word is not None:
            on_each_word(vocab)

    return vocab_list


def scrape_word(word: str) -> Vocab:
    url = f"{base_def_url}/{word}"
    response = requests.get(url)

    res_json_str = response.text

    soup = BeautifulSoup(res_json_str, "html.parser")

    for a in soup.findAll('a'):
        a.replace_with("%s" % a.string)

    loaded_json = json.loads(soup.text)
    if loaded_json is None or "en" not in loaded_json:
        return Vocab(word=word)
    types = loaded_json["en"]

    type_list: list[WordType] = []

    for type in types:
        word_type_definition: list[WordTypeDefinition] = []

        for item in type["definitions"]:

            definition = item["definition"]
            examples: list[str] = []
            if "examples" in item:
                examples = item["examples"]

            word_type_definition.append(
                WordTypeDefinition(
                    definition=definition,
                    examples=examples
                )
            )

        word_type = WordType(
            word_type=type["partOfSpeech"],
            word_type_definitions=word_type_definition
        )
        type_list.append(word_type)

    return Vocab(
        word=word,
        word_type=type_list
    )


if __name__ == '__main__':
    run_scraper()
