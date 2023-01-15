def _word_url(word: str) -> str:
    base_url = "https://en.wiktionary.org/api/rest_v1/page/definition"
    return base_url + '/' + word

