from src.scraper.manage_scraper import manage_scraper
from src.utils.FileHelper import FileHelper

if __name__ == '__main__':
    manage_scraper(
        word_filepath=FileHelper.current_dir('../raw/words_alpha.txt'),
        workspace_directory=FileHelper.current_dir('../workspace'),
    )
