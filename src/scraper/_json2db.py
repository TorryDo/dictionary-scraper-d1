import sqlite3

from src.model.vocab.vocab import Vocab
from src.utils.FileHelper import FileHelper
from src.utils.JsonHelper import JsonHelper


def _json2db(table_name: str, vocab_jsons: list[str], dst: str):
    if not FileHelper.is_existed(dst):
        FileHelper.create_file(dst)
    connection = sqlite3.connect(dst)
    cursor = connection.cursor()
    cursor.execute(
        f'Create Table if not exists {table_name} (id Integer Not Null PRIMARY KEY, word Text Not Null, types Text Not Null)'
    )

    for vocab_json in vocab_jsons:
        vocab_dict = JsonHelper.str2dict(vocab_json)
        word = vocab_dict['word']
        types = JsonHelper.dict2json(vocab_dict['types'])

        params = (word, str(types))
        cursor.execute(f"INSERT INTO {table_name}(word, types) values(?, ?)", params)

    connection.commit()
    connection.close()