import asyncio



def asleep(sec: float):
    """
    async sleep, this function shorten the code below
    asyncio.run(asyncio.sleep(sec))
    """
    asyncio.run(asyncio.sleep(sec))  # this function will suspend
    # time.sleep(sec)              # this function caused print work improperly


def run_async(job):
    """
    :job: a function
    run async task simultaneously (not await)
    """
    asyncio.get_event_loop().create_task(job())
