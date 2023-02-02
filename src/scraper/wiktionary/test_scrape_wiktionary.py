from unittest import TestCase, IsolatedAsyncioTestCase

from src.scraper.wiktionary.scrape_wiktionary import scrape_wiktionary_word


class Test(IsolatedAsyncioTestCase):
    async def test_scrape_wiktionary_word(self):
        word = 'star'
        vocab1 = await scrape_wiktionary_word(word)
        self.assertTrue(vocab1 is not None)

        word2 = 'sdfadfs'
        vocab2 = await scrape_wiktionary_word(word2)
        self.assertTrue(vocab2 is None)

        word3 = 'exomion'
        vocab3 = await scrape_wiktionary_word(word3)
        vocab3.print()
        self.assertTrue(vocab3 is not None)

        word4 = 'expand'
        vocab4 = await scrape_wiktionary_word(word4)
        vocab4.print()
        self.assertTrue(vocab4 is not None)
