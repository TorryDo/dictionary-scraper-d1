import asyncio
import time
from pathlib import Path

from src.utils.FileHelper import FileHelper


# for i in tqdm(range(0, 100), desc="scraping", unit='mb'):
#     sleep(.1)

async def heavy_task(t) -> int:
    begin = time.time()
    print("start task...")
    await asyncio.sleep(t)
    end = time.time()
    time_exec = end - begin
    print(f"finish task after: {time_exec}!")
    return t


async def wrapper(f):
    await f()


async def main():
    tasks = await asyncio.gather(*[heavy_task(_) for _ in range(5)])


if __name__ == '__main__':
   Path(FileHelper.current_dir('hello')).mkdir()
