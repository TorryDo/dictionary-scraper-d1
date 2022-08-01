import asyncio

loop = asyncio.get_event_loop()


async def to_async(task):
    future = loop.run_in_executor(None, task)
    return await future
