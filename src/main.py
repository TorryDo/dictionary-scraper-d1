import time

import wik_def_scraper as wik
from files.path import words_file_path
from src.model.vocab.vocab import Vocab

start_time = time.time()

with open(words_file_path) as f:
    words = [line.rstrip() for line in f.readlines()]

    sub_words = words[0:25]

    vocab_list: list[Vocab] = wik.run_scraper(sub_words, accept_empty_word=False)



print(f"\n<>Crawler took: {(time.time() - start_time).__round__(3)}s to run")
