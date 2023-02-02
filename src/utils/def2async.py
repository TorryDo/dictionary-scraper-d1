import asyncio
from functools import partial, wraps


def to_async(func):
    @wraps(func)  # Makes sure that function is returned for e.g. func.__name__ etc.
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_running_loop()  # Make event loop of nothing exists
        pfunc = partial(func, *args, **kwargs)  # Return function with variables (event) filled in
        return await loop.run_in_executor(executor, pfunc)

    return run
