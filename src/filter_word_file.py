from src.utils.FileHelper import FileHelper

filepath = 'C:/Users/trido/Desktop/python/wiktionary_scraper/assets/data/most_used_100k_english.txt'

if __name__ == '__main__':
    lines = FileHelper.lines(filepath)
    word_set = set()
    for line in lines:
        if line.startswith('#') or line.startswith("'"):
            continue
        if not line.isalpha() and "'" not in line:
            print(f'- ignore: "{line}"')
            continue
        word_set.add(line.lower())

    base_word_set = set(FileHelper.lines('C:/Users/trido/Desktop/python/wiktionary_scraper/raw/words_alpha.txt'))

    result = [x for x in word_set if x in base_word_set]
    result.sort()

    word_data = '\n'.join(result)

    FileHelper.write_text_file(
        path='C:/Users/trido/Desktop/python/wiktionary_scraper/assets/data/most_used_100k_english.txt',
        data=word_data
    )
