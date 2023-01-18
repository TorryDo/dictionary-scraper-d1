from enum import Enum


class ScrapingState(Enum):
    Initialized = 'initialized'
    Scraped = 'scraped'
    Finalized = 'finalized'
    Finished = 'finished'


if __name__ == '__main__':
    pass
