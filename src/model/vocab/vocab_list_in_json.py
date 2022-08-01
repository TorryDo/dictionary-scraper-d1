#
from enum import Enum

from src.model.vocab.vocab import Vocab


class Language(Enum):
    English = 'eng'
    Vietnamese = 'vi'


class VocabListInJson:
    language: Language = Language.English
    vocab_list: list[Vocab] = []

    def __init__(self, language: Language = Language.English, words: list[Vocab] = None):
        self.language = language
        if words is not None and len(words) > 0:
            self.vocab_list = words

    def toJson(self) -> str:
        words_in_json = '['
        for word in self.vocab_list:
            words_in_json += f'{word.toJson()},'

        words_in_json = words_in_json.removesuffix(',')
        words_in_json += ']'

        return f'{{"language": "{self.language.value}", "words":{words_in_json}}}'
