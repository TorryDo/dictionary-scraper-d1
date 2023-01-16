import asyncio
import inspect
import time

from src.ext.def_to_async import to_async


class AsyncHelper:

    @staticmethod
    def run_async_tasks(funcs):
        # is_async = inspect.iscoroutinefunction(object)

        async def wrapper():
            async_tasks = list()

            for func in funcs:
                # is_async = inspect.iscoroutinefunction(func)
                # f = func if is_async else await to_async(func)
                async_tasks.append(asyncio.create_task(func()))

            await asyncio.wait(async_tasks)

        asyncio.run(wrapper())


if __name__ == '__main__':
    async def _slow_task():
        await asyncio.sleep(1)
        print('hello')


    l = []
    for i in range(5):
        l.append(_slow_task)
    AsyncHelper.run_async_tasks(l)
