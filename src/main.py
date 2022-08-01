import time

import wik_def_scraper as wik
from src.model.vocab.vocab import Vocab
from src.model.vocab.vocab_list_in_json import VocabListInJson, Language

start_time = time.time()

vocab_list_in_json: VocabListInJson = VocabListInJson(language=Language.English)

words_file_path = "../raw/words_alpha.txt"

with open(words_file_path) as f:
    words = [line.rstrip() for line in f.readlines()]

    sub_words = words[0:10]

    vocab_list: list[Vocab] = wik.scrape_words(sub_words, accept_empty_word=False)
    vocab_list_in_json.vocab_list = vocab_list

    print(vocab_list_in_json.toJson())

print(f"\n<>Crawler took: {(time.time() - start_time).__round__(3)}s to run")
