from src.model.base.printable import Printable
from src.model.vocab.word_type import WordPart


class Vocab(Printable):
    word: str = None
    word_parts: list[WordPart] = []

    def __init__(
            self,
            word: str,
            word_types: list[WordPart] = None
    ):
        self.word = word
        if word_types is not None:
            self.word_parts = word_types

    def print(self, prefix: str = "-"):
        print(f"{prefix} word: {self.word}")
        for item in self.word_parts:
            item.print()

    def to_str(self) -> str:
        result = ""

        word_type_str = ""
        if len(self.word_parts) > 0:
            for item in self.word_parts:
                word_type_str += item.to_str()

        result += self.word
        result += word_type_str

        return result

    def toJson(self) -> str:

        types_in_json = '['
        for type in self.word_parts:
            types_in_json += type.toJson()
            types_in_json += ','

        types_in_json = types_in_json.removesuffix(',')
        types_in_json += ']'

        return f'{{"word": "{self.word}", "parts": {types_in_json} }}'


########################################################################################################################
def to_array_json(vocab_list: list[Vocab]) -> str:
    result = '['

    for vocab in vocab_list:
        result += vocab.toJson() + ','

    result = result.removesuffix(',')
    result += ']'

    return result
