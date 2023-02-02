from src.model.base.printable import Printable
from src.model.vocab.word_type_definition import WordTypeDefinition


class WordPart(Printable):
    type: str = None
    definitions: list[WordTypeDefinition] = []

    def __init__(self, word_type: str, word_type_definitions: list[WordTypeDefinition]):
        self.type = word_type
        self.definitions = word_type_definitions

    def print(self, prefix: str = "-"):
        print(f"{prefix} type: {self.type}")
        for item in self.definitions:
            item.print()

    def to_str(self) -> str:
        result = ""

        result += self.type

        for item in self.definitions:
            result += item.definition

        return result

    # def toJson(self) -> str:
    #     return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)

    def toJson(self) -> str:

        temp = ','.join([definition.toJson() for definition in self.definitions])
        definitions_in_json = f'[{temp}]'

        return f'{{"name": "{self.type.lower()}", "defs": {definitions_in_json}}}'
