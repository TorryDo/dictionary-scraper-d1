from src.model.vocab.vocab import Vocab
from src.wik_def_crawler import crawl_word

words = ["star", "prolong", "dictionary", "future"]

for word in words:
    vocab: Vocab = crawl_word(word)

    jsonStr = vocab.toJson()

    print(jsonStr)
