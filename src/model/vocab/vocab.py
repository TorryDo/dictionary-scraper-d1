import json
from enum import Enum

from src.model.base.printable import Printable
from src.model.vocab.word_type import WordType


class Language(Enum):
    English = "eng"
    Vietnamese = "vi"


# english = "english"
# vietnamese = "vietnamese"


class Vocab(Printable):
    word: str = None
    lang: Language = Language.English
    word_type: list[WordType] = []

    def __init__(
            self,
            word: str,
            language: Language = Language.English,
            word_type: list[WordType] = None
    ):
        self.word = word
        self.lang = language
        if word_type is not None:
            self.word_type = word_type

    def print(self, prefix: str = "-"):
        print(f"{prefix} word: {self.word}")
        print(f"{prefix} language: {self.lang.name}")
        for item in self.word_type:
            item.print()

    def to_str(self) -> str:
        result = ""

        word_type_str = ""
        if len(self.word_type) > 0:
            for item in self.word_type:
                word_type_str += item.to_str()

        result += self.word
        result += self.lang.name
        result += word_type_str

        return result

    def toJson(self) -> str:

        types_in_json = '['
        for type in self.word_type:
            types_in_json += type.toJson()
            types_in_json += ','

        types_in_json += ']'

        return f'{{"word": {self.word}, "lang": {self.lang.value}, "types": {types_in_json} }}'
