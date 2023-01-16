import shutil

from src.scraper.properties import ScraperProps
from src.utils.FileHelper import FileHelper


def move_files_from_queue_to_split():
    queue_dir = ScraperProps.scrape_queue_dir
    queue_filepaths = [f'/{name}' for name in FileHelper.children(from_root=queue_dir)]

    for src_name in queue_filepaths:
        shutil.move(
            src=queue_dir + f'/{src_name}',
            dst=ScraperProps.split_words_dir + f'/{src_name}'
        )
