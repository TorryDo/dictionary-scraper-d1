class ScraperProps:
    scraper_number: int
    word_filepath: str
    workspace_dir: str
    config_filepath: str

    result_dir: str
    error_words_dir: str
    success_words_dir: str
    result_error_txt_filepath: str
    result_success_jsontxt_filepath: str

    wip_dir: str
    split_words_dir: str
    scrape_queue_dir: str

    on_start = None
    in_progress = None
    on_finished = None

    split_filename_prefix = '_'
