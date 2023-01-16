from unittest import TestCase

from src.scraper.wiktionary.scrape_wiktionary import scrape_wiktionary_word


class Test(TestCase):
    def test_scrape_wiktionary_word(self):
        word = 'star'
        vocab1 = scrape_wiktionary_word(word)
        self.assertTrue(vocab1 is not None)

        word2 = 'sdfadfs'
        vocab2 = scrape_wiktionary_word(word2)
        self.assertTrue(vocab2 is None)
