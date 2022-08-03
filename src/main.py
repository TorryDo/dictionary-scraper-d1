import wik_def_scraper as wik
from src.base.base import root_dir
from src.model.vocab.vocab_list_in_json import VocabListInJson, Language

vocab_list_in_json: VocabListInJson = VocabListInJson(language=Language.English)

wik.scrape(
    word_file_path=root_dir(child='/raw/words_alpha.txt'),
    workspace_dir_path=root_dir(child='/files/cache'),
    accept_empty_word=False,
    parallel=10
)
