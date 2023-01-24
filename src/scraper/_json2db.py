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
        f'CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER NOT NULL PRIMARY KEY, word TEXT NOT NULL, parts_json TEXT NOT NULL)'
    )

    for vocab_json in vocab_jsons:
        vocab_dict = JsonHelper.str2dict(vocab_json)
        word = vocab_dict['word']
        types = vocab_dict['parts']

        new_types = JsonHelper.dict2json(types)

        params = (word, new_types)
        cursor.execute(f"INSERT INTO {table_name}(word, parts_json) values(?, ?)", params)

    connection.commit()
    connection.close()
