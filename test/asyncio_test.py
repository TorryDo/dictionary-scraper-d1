import asyncio
import random

count = 0

strList: list[str] = []

for i in range(20):
    strList.append(str(i))

thr_num = 3


async def do_task():
    try:
        if len(strList) == 0:
            print('end of list')
            return

        await asyncio.sleep(random.randrange(1, 4))

        if len(strList) > 0:
            print(strList[0])
            strList.pop(0)
            await do_task()


    except NameError:
        pass


# async def func(num):
#     print('Starting func {0}...'.format(num))
#     await asyncio.sleep(1)
#     print('Ending func {0}...'.format(num))


loop = asyncio.get_event_loop()


async def create_tasks_func():
    tasks = list()
    for i in range(20):
        tasks.append(asyncio.create_task(do_task()))
    await asyncio.wait(tasks)


loop.run_until_complete(create_tasks_func())
loop.close()
