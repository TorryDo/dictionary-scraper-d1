# it takes < 2sec to load and print 370k words from text file
import time

from src.base.file_helper import get_all_path_with_prefix
from src.split_file import split_huge_text_file_to_multiple_smaller_file

if __name__ == '__main__':
    start_time = time.time()
    split_huge_text_file_to_multiple_smaller_file(
        source_path='../raw/words_alpha.txt'
    )

    print(get_all_path_with_prefix(
        folder_path='../files/cache/splitter',
        prefix='_'
    ))

    print(f"\n<>Split file took: {(time.time() - start_time).__round__(3)}s to run")
