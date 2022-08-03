import wik_def_scraper as wik
from src.model.vocab.vocab_list_in_json import VocabListInJson, Language

vocab_list_in_json: VocabListInJson = VocabListInJson(language=Language.English)

wik.scrape(
    word_file_path='C:\\Users\\trido\\Desktop\\scrape\\wiktionary\\words_alpha.txt',
    workspace_dir_path='C:\\Users\\trido\\Desktop\\scrape\\wiktionary\\cache',
    accept_empty_word=False,
    parallel=8
)
