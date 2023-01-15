class ScraperProps:
    scraper_number: int
    word_filepath: str
    workspace_dir: str
    config_filepath: str
    result_dir: str
    error_words_dir: str
    success_words_dir: str

    wip_dir: str
    extract_words_dir: str
    split_words_dir: str

    in_progress = None
    on_finished = None

    split_filename_prefix = '_'


class ConfigKeys:
    word_file_path = 'word_file_path'
    word_number = 'word_number'
    in_progress = 'in_progress'
    total_split_file_number = 'total_split_file_number'
    result = 'result'
    success_word_number = 'success_word_number'
    error_word_number = 'error_word_number'


"""
config.txt structure:
{
    word_file_path: string,
    word_number: int,
    in_progress: {
        // current_split_file_number: int,
        total_split_file_number: int
    },
    result: {
        success_word_number: int,
        error_word_number: int
    }   
}
"""
