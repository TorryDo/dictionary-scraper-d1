import os.path
import sys


def root_dir(
        child: str = None
) -> str:
    result = ''

    result += sys.path[1].replace('\\', '/')

    # result += os.path.expanduser(path=)

    if child is not None:
        result += child

    return result
