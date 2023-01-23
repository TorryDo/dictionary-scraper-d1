import sqlite3
import time

from src.utils.FileHelper import FileHelper
from src.utils.JsonHelper import JsonHelper


def _json2db(table_name: str, vocab_jsons: list[str], dst: str):

    if not FileHelper.is_existed(dst):
        FileHelper.create_file(dst)
    connection = sqlite3.connect(dst)
    cursor = connection.cursor()
    cursor.execute(
        f'CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER NOT NULL PRIMARY KEY, word TEXT NOT NULL, types TEXT NOT NULL)'
    )

    for vocab_json in vocab_jsons:
        vocab_dict = JsonHelper.str2dict(vocab_json)
        word = vocab_dict['word']
        types = vocab_dict['types']

        # remove empty examples in types
        for type in types:
            definitions = type['definitions']
            for definition in definitions:
                examples = definition.get('examples')
                if examples is not None and len(examples) == 0:
                    definition.pop('examples')

        # shorten keys
        # short_key_types: list = []
        # for _type in types:
        #     short_type = {
        #         'type': _type['type'],
        #         'defs': []
        #     }
        #     for _def in _type['definitions']:
        #         short_definition = _def['definition']
        #         short_examples = _def.get('examples')
        #         short_def = {
        #             'def': short_definition
        #         }
        #         if short_examples is not None and len(short_examples) >= 0:
        #             short_def['egs'] = short_examples
        #         short_type['defs'].append(short_def)
        #     short_key_types.append(JsonHelper.dict2json(short_type))
        # _dkm = '[' + ','.join(short_key_types) + ']'

        new_types = JsonHelper.dict2json(types)

        params = (word, str(new_types))
        cursor.execute(f"INSERT INTO {table_name}(word, types) values(?, ?)", params)

    connection.commit()
    connection.close()
