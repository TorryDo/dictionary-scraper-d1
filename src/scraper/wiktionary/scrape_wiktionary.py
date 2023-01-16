from typing import Optional

import requests
from bs4 import BeautifulSoup

from src.model.vocab.vocab import Vocab
from src.model.vocab.word_type import WordType
from src.model.vocab.word_type_definition import WordTypeDefinition
from src.utils.JsonHelper import JsonHelper


def _word_url(word: str) -> str:
    base_url = "https://en.wiktionary.org/api/rest_v1/page/definition"
    return f'{base_url}/{word}'


def scrape_wiktionary_word(
        word: str,
        on_status_code=None,
) -> Optional[Vocab]:
    url = _word_url(word)
    response = requests.get(url)

    if response.status_code >= 400:
        if on_status_code is not None:
            on_status_code()
        return None

    # remove tag inside text
    json_data = BeautifulSoup(response.text, "html.parser").text

    print(json_data)

    # start scrape content
    cock = JsonHelper.str2dict(json_data)
    if len(cock) == 0 or "en" not in cock:
        return None

    type_list: list[WordType] = []

    for word_type_cock in cock["en"]:
        typedef_list: list[WordTypeDefinition] = []

        for item in word_type_cock["definitions"]:
            typedef_list.append(WordTypeDefinition(
                definition=item["definition"],
                examples=item['examples'] if ('examples' in item) else []
            ))

        word_type = WordType(
            word_type=word_type_cock["partOfSpeech"],
            word_type_definitions=typedef_list
        )
        type_list.append(word_type)

    return Vocab(word=word, word_types=type_list)
