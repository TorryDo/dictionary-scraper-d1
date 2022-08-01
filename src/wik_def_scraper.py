# wiktionary definition scraper
import asyncio
import json
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
from src.ext.def_to_async import to_async
from src.model.vocab.vocab import Vocab
from src.model.vocab.word_type import WordType
from src.model.vocab.word_type_definition import WordTypeDefinition
from src.split_file import split_huge_text_file_to_multiple_smaller_file

base_def_url = "https://en.wiktionary.org/api/rest_v1/page/definition"

words_alpha_txt = root_dir('/raw/words_alpha.txt')

splitter_dir_path = root_dir(child='/files/cache/splitter')
config_file_path = splitter_dir_path + '/config.txt'
temp_splitter_dir_path = root_dir(child='/files/cache/temp_splitter')

temp_data_mine_dir_path = root_dir(child='/files/cache/temp_data_mine')
data_mine_dir_path = root_dir(child='/files/data_mine')


def scrape():
    split_huge_text_file_to_multiple_smaller_file(
        source_path=words_alpha_txt,
        _splitter_dir_path=splitter_dir_path,
        each_word_per_file=200,
        prefix_each_file='_'
    )

    move_all_from_temp_splitter_to_splitter_if_exists()

    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run_scraper_in_parallel(
            words_file_path=root_dir('/raw/words_alpha.txt'),
            parallel=10
        ))
        loop.close()
    except NameError:
        print(NameError)

    print('scrape finished')

    on_finished()


def move_all_from_temp_splitter_to_splitter_if_exists():
    previous_temp_file_words: list[str] = get_all_path_with_prefix(folder_path=temp_splitter_dir_path, prefix='_')

    if len(previous_temp_file_words) == 0:
        return

    while len(previous_temp_file_words) > 0:
        first_name = previous_temp_file_words[0]
        previous_temp_file_words.pop(0)

        src_temp_word_file_path = temp_splitter_dir_path + '/' + first_name
        dst_temp_word_file_path = splitter_dir_path + '/' + first_name

        shutil.move(
            src=src_temp_word_file_path,
            dst=dst_temp_word_file_path
        )


def on_finished():
    print('start concatenate files')

    result: str = '['

    temp_word_file_names = get_all_path_with_prefix(folder_path=root_dir('/files/cache/temp_data_mine'))

    for word_file_name in temp_word_file_names:
        full_path = temp_data_mine_dir_path + '/' + word_file_name
        lines = read_each_line(path=full_path)
        for line in lines:
            result += line + '\n'

    result = result.removesuffix(',\n')
    result += ']'
    print('finish concatenate files')


async def run_scraper_in_parallel(
        words_file_path: str = words_alpha_txt,
        accept_empty_word: bool = True,
        parallel: int = 5,
        progress=None
):
    create_dir_if_not_exists(dir_path=temp_splitter_dir_path)

    split_word_file_name_list: list[str] = get_all_path_with_prefix(folder_path=splitter_dir_path, prefix='_')

    if len(split_word_file_name_list) == 0:
        print('job finished')
        return

    while len(split_word_file_name_list) > 0:

        move_all_from_temp_splitter_to_splitter_if_exists()

        tasks = list()
        for _ in range(parallel):

            if len(split_word_file_name_list) == 0:
                break

            first_name = split_word_file_name_list[0]
            split_word_file_name_list.pop(0)

            src_temp_word_file_path = splitter_dir_path + '/' + first_name
            dst_temp_word_file_path = temp_splitter_dir_path + '/' + first_name
            temp_data_mine_file_path = temp_data_mine_dir_path + '/' + first_name

            tasks.append(asyncio.create_task(scrape_word_then_move_file(
                src_path=src_temp_word_file_path,
                dst_path=dst_temp_word_file_path,
                temp_data_mine_path=temp_data_mine_file_path
            )))
        await asyncio.wait(tasks)


async def scrape_word_then_move_file(
        src_path: str,
        dst_path: str,
        temp_data_mine_path: str
) -> bool:
    try:
        shutil.move(src=src_path, dst=dst_path)

        vocab_list: list[Vocab] = await to_async(task=lambda: scrape_words(
            words=read_each_line(path=dst_path),
            accept_empty_word=False
        ))

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
    scrape()
