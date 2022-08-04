import json
import sqlite3


def json_to_db(db_file_path: str):
    table_name = 'WordDefinition'

    connection = sqlite3.connect(db_file_path)
    cursor = connection.cursor()
    cursor.execute(
        f'Create Table if not exists {table_name} (id Integer Not Null, word Text Not Null, types Text Not Null)')

    traffic = json.load(open('C:/Users/trido/Desktop/scrape/wiktionary/cache/data_mine/words.txt'))

    temp_id = 1

    for row in traffic:
        id = temp_id
        word = row['word']
        types = row['types']

        keys = tuple((id, word, str(types)))

        cursor.execute(f'insert into {table_name} values(?,?,?)', keys)

        temp_id += 1

    connection.commit()
    connection.close()


if __name__ == '__main__':
    json_to_db(db_file_path='C:/Users/trido/Desktop/scrape/wiktionary/eng_words_id.db')
