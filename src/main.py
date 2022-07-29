import time

import wik_def_scraper as wik
from path.path import folder_path, scarped_words_file_name, words_file_path
from src.model.vocab.vocab_list_in_json import VocabListInJson, Language

start_time = time.time()

file_path = f"{folder_path}\\{scarped_words_file_name}"

file = open(file_path, "w", encoding="utf-8")

vocab_list_in_json: VocabListInJson = VocabListInJson(language=Language.English)


with open(words_file_path) as f:
    words = [line.rstrip() for line in f]

    sub_words = words[0:1000]

    vocab_list_in_json.words = wik.scrape_words(sub_words, accept_empty_word=False)


print(vocab_list_in_json.toJson())

file.write(vocab_list_in_json.toJson())

print(f"\n<>Crawler took: {(time.time() - start_time).__round__(3)}s to run")
