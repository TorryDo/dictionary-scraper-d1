import json

from src.model.base.printable import Printable


class WordTypeDefinition(Printable):
    definition: str = None
    examples: list[str] = []

    def __init__(self, definition: str, examples: list[str]):
        self.definition = definition
        self.examples = examples

    def print(self, prefix: str = "-"):
        print(f"{prefix} definition: {self.definition}")
        self.print_examples(prefix=prefix)

    def print_examples(self, prefix: str = "-"):
        if self.examples is not None and len(self.examples) > 0:
            for example in self.examples:
                print(f"{prefix} examples: {example}")

    def to_str(self) -> str:
        if self.examples is not None and len(self.examples) > 0:
            result = ""
            result += self.definition
            for example in self.examples:
                result += f"--- examples: {example}"
        else:
            return ""

    def toJson(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)

    # def toJson(self) -> str:
    #
    #     examples_in_json = '['
    #
    #     for example in self.examples:
    #         examples_in_json += f'{example},'
    #
    #     examples_in_json = examples_in_json.removesuffix(',')
    #     examples_in_json += ']'
    #
    #     return f'{{"definition": {self.definition}, "examples": {examples_in_json}}}'
