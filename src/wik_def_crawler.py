# wiktionary definition crawler
import json

import requests
from bs4 import BeautifulSoup

from src.model.vocab.vocab import Vocab, Language
from src.model.vocab.word_type import WordType
from src.model.vocab.word_type_definition import WordTypeDefinition

base_word_url = "https://en.wiktionary.org/api/rest_v1/page/definition"


def crawl_word(word: str) -> Vocab:
    url = f"{base_word_url}/{word}"
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
        language=Language.English,
        word_type=type_list
    )
