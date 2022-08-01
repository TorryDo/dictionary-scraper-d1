import asyncio
import random
import time

from src.ext.def_to_async import to_async

count = 0

strList: list[str] = []

for i in range(20):
    strList.append(str(i))

thr_num = 3


def fake_task():
    time.sleep(random.randrange(1, 4))


async def do_task():
    try:
        if len(strList) == 0:
            print('end of list')
            return

        await to_async(task=fake_task)

        if len(strList) > 0:
            print(strList[0])
            strList.pop(0)
            await do_task()


    except NameError:
        pass


loop = asyncio.get_event_loop()


async def create_tasks_func():
    tasks = list()
    for i in range(20):
        tasks.append(asyncio.create_task(do_task()))
    await asyncio.wait(tasks)


loop.run_until_complete(create_tasks_func())
loop.close()
