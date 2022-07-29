from src.model.vocab.vocab import Vocab
from src.wik_def_scraper import scrape_word

words = ["star", "prolong", "dictionary", "future"]

for word in words:
    vocab: Vocab = scrape_word(word)

    jsonStr = vocab.toJson()

    print(jsonStr)
