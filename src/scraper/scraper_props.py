from src.scraper.ScrapeSource import ScrapeSource


class ScraperProps:
    scraper_number: int
    word_filepath: str
    workspace_dir: str
    config_filepath: str = None
    scraper_number: int = None
    scrape_source: ScrapeSource = None

    workspace_filepath: str = None

    result_dir: str
    error_words_dir: str
    success_words_dir: str
    result_error_txt_filepath: str
    result_success_jsontxt_filepath: str

    wip_dir: str
    split_words_dir: str
    scrape_queue_dir: str

    on_init = None
    on_start_scraping = None
    in_progress = None
    on_finished = None

    split_filename_prefix = '_'
