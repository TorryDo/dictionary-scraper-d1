import asyncio
import json
import shutil
import threading
import time
import warnings

import requests
from bs4 import BeautifulSoup

from src.ext.def_to_async import to_async
from src.ext.file_helper import (
    get_all_path_with_prefix,
    create_dir_if_not_exists,
    read_each_line,
    write_txt_file,
    remove_file, is_exist
)
from src.model.vocab.vocab import Vocab
from src.model.vocab.word_type import WordType
from src.model.vocab.word_type_definition import WordTypeDefinition
from src.split_file import split_huge_text_file_to_multiple_smaller_file, write_config_file

base_def_url = "https://en.wiktionary.org/api/rest_v1/page/definition"

words_file_path = ''

config_file_path = ''
splitter_dir_path = ''
temp_splitter_dir_path = ''

data_mine_dir_path = ''
temp_data_mine_dir_path = ''

total_file_word = 0


def scrape(
        word_file_path: str,
        workspace_dir_path: str = '',
        accept_empty_word: bool = False,
        parallel: int = 5,
):
    # check if file satisfy condition

    word_file_path = word_file_path.replace('\\', '/')
    workspace_dir_path = workspace_dir_path.replace('\\', '/')

    if not is_exist(word_file_path):
        raise Exception(f'file words: "{word_file_path}" is not exist')
    if not is_exist(path=workspace_dir_path):
        raise Exception(f'folder: "{workspace_dir_path}" is not created')

    # set paths and create if not exist
    global words_file_path
    global config_file_path
    global splitter_dir_path
    global temp_splitter_dir_path
    global data_mine_dir_path
    global temp_data_mine_dir_path
    global total_file_word

    words_file_path = word_file_path
    splitter_dir_path = workspace_dir_path + '/splitter'
    temp_splitter_dir_path = workspace_dir_path + '/temp_splitter'
    config_file_path = workspace_dir_path + '/config.txt'
    data_mine_dir_path = workspace_dir_path + '/data_mine'
    temp_data_mine_dir_path = workspace_dir_path + '/temp_data_mine'

    create_dir_if_not_exists(dir_path=splitter_dir_path)
    create_dir_if_not_exists(dir_path=temp_splitter_dir_path)
    create_dir_if_not_exists(dir_path=data_mine_dir_path)
    create_dir_if_not_exists(dir_path=temp_data_mine_dir_path)

    # split file if first time launch
    if not is_exist(config_file_path):
        print('splitting given word file... (only run on first launch)')
        split_huge_text_file_to_multiple_smaller_file(
            words_file_path=words_file_path,
            dst_dir_path=splitter_dir_path,
            each_word_per_file=200,
            prefix_each_file='_'
        )
        config_data = words_file_path + '\n'
        file_number = get_all_path_with_prefix(
            folder_path=splitter_dir_path,
            prefix='_'
        )
        config_data += str(len(file_number)) + '\n'

        # should change this function later
        write_config_file(
            file_path=config_file_path,
            data=config_data
        )
        print('split file succeed')

    warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

    total_file_word = int(read_each_line(path=config_file_path)[1])

    move_all_from_temp_splitter_to_splitter_if_exists()

    remained_file = get_all_path_with_prefix(splitter_dir_path, '_')
    if len(remained_file) == 0:
        print('finalizing')
        on_finished()
        return

    threading.Thread(target=calc_progress).start()

    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            future=run_scraper_in_parallel(
                accept_empty_word=accept_empty_word,
                parallel=parallel
            ))
        loop.close()
    except NameError:
        print(NameError)

    print('scrape finished')

    on_finished()


def on_finished():
    result_words_txt = data_mine_dir_path + '/words.txt'
    result_error_words_txt = data_mine_dir_path + '/error_words.txt'

    total_words = read_each_line(path=words_file_path)
    scraped_words = set()
    error_words = list[str]()

    if is_exist(result_words_txt) and is_exist(result_error_words_txt):

        error_words = read_each_line(path=result_error_words_txt)
        scraped_words = read_each_line(result_words_txt)

        scraped_words.pop(0)
        scraped_words.pop(len(scraped_words) - 1)

    else:

        start_time = time.time()
        print('merging files, please wait...')

        temp_word_file_names = get_all_path_with_prefix(folder_path=temp_data_mine_dir_path, prefix='_')

        result: str = '[\n'

        scrape_word_file = data_mine_dir_path + '/words.txt'

        for word_file_name in temp_word_file_names:
            full_path = temp_data_mine_dir_path + '/' + word_file_name
            lines = read_each_line(path=full_path)
            for line in lines:
                result += line + '\n'
                word = json.loads(line.removesuffix('\n').removesuffix(','))['word']
                scraped_words.add(word)

        result = result.removesuffix('\n').removesuffix(',')
        result += '\n]'

        write_txt_file(path=scrape_word_file, data=result)

        error_words = [item for item in total_words if item not in scraped_words]

        error_words_data = ''
        for error_word in error_words:
            error_words_data += error_word + '\n'
        error_words_data = error_words_data.removesuffix('\n')

        write_txt_file(path=result_error_words_txt, data=error_words_data)
        print(f'finish concatenate files, took: {round(time.time() - start_time, ndigits=3)}s')

    #

    print(f'total word = {len(total_words)}')
    print(f'scraped word = {len(scraped_words)}')
    print(f'error word = {len(error_words)}')


def calc_progress():
    old_result: float = 0

    while old_result <= 0.99:
        if total_file_word == 0:
            time.sleep(15)
            continue

        current = len(get_all_path_with_prefix(folder_path=temp_data_mine_dir_path, prefix='_'))

        result = round(number=(current / total_file_word), ndigits=2)

        if result > old_result:
            print(f'progress: {int(result * 100)}/100')
            old_result = result

        time.sleep(15)

    print('finalizing...')


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


async def run_scraper_in_parallel(
        accept_empty_word: bool,
        parallel: int = 5
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
                temp_data_mine_path=temp_data_mine_file_path,
                accept_empty_word=accept_empty_word
            )))
        await asyncio.wait(tasks)


async def scrape_word_then_move_file(
        src_path: str,
        dst_path: str,
        temp_data_mine_path: str,
        accept_empty_word: bool
) -> bool:
    try:
        shutil.move(src=src_path, dst=dst_path)

        vocab_list: list[Vocab] = await to_async(task=lambda: scrape_words(
            words=read_each_line(path=dst_path),
            accept_empty_word=accept_empty_word
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
        return False


def scrape_words(
        words: list[str],
        accept_empty_word: bool = True,
) -> list[Vocab]:
    #
    vocab_list: list[Vocab] = []

    for word in words:
        try:
            vocab = scrape_word(word)

            if accept_empty_word:
                vocab_list.append(vocab)
            else:
                if len(vocab.word_type) > 0:
                    vocab_list.append(vocab)
        except NameError:
            continue

    return vocab_list


def scrape_word(word: str) -> Vocab:
    url = f"{base_def_url}/{word}"
    response = requests.get(url)

    if response.status_code == 404:
        # print(f'word 404: {word}')
        return Vocab(word=word)

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

# if __name__ == '__main__':
#     scrape(
#         word_file_path=root_dir(child='/raw/words_alpha.txt'),
#         cache_dir_path=root_dir(child='/files/cache'),
#         result_data_dir_path=root_dir(child='/files/data_mine'),
#         accept_empty_word=False,
#         parallel=10
#     )
