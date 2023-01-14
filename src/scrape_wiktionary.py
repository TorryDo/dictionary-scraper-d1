from src.utils.FileHelper import FileHelper


def _word_url(word: str) -> str:
    base_url = "https://en.wiktionary.org/api/rest_v1/page/definition"
    return base_url + '/' + word


_workspace_dir: str
_word_filepath: str
_scraper_number: int


def scrape_wiktionary(
        word_filepath: str,
        workspace_directory: str = FileHelper.current_dir('../workspace'),
        scraper_number: int = 5,
        in_progress=None,
        on_finished=None,
):
    if not FileHelper.is_existed(word_filepath):
        raise Exception(f'file: {word_filepath} not existed')
    if not FileHelper.is_existed(workspace_directory):
        if len(FileHelper.children(workspace_directory)) > 0:
            raise Exception(f'directory: {workspace_directory} must be empty')
    else:
        FileHelper.mkdir(workspace_directory)

    global _word_filepath
    global _workspace_dir
    global _scraper_number
    _scraper_number = scraper_number
    _word_filepath = word_filepath
    _workspace_dir = workspace_directory



if __name__ == '__main__':
    pass
