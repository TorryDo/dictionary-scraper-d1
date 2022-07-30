# wiktionary definition scraper
import json

import requests
from bs4 import BeautifulSoup

from src.model.vocab.vocab import Vocab
from src.model.vocab.word_type import WordType
from src.model.vocab.word_type_definition import WordTypeDefinition

base_def_url = "https://en.wiktionary.org/api/rest_v1/page/definition"
finished_words_file_path = "../files/cache/finished_words.txt"
mined_words_file_path = "../files/data_mine/words.txt"

check_words: list[str] = []
check_words_file = open(finished_words_file_path, mode='a+', encoding='utf-8')
check_words_file.seek(0)
check_words_list = [line.rstrip() for line in check_words_file.readlines()]

for word in check_words_list:
    check_words.append(word)

file_words = open(mined_words_file_path, "w", encoding="utf-8")

if __name__ == "__main__":
    print(check_words)

    quit()


def run_scraper(
        words: list[str],
        accept_empty_word: bool = True,
) -> list[Vocab]:
    filter_words = [x for x in words if x not in check_words]

    result: list[Vocab] = []

    if len(filter_words) == 0:
        print("all words are scraped 😎")
    else:
        result = scrape_words(
            words=filter_words,
            accept_empty_word=accept_empty_word
        )

    cache_word: str = ''
    for item in result:
        cache_word += item.word
        cache_word += '\n'

    check_words_file.write(cache_word)

    return result


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
