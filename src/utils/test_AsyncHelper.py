import asyncio
from unittest import TestCase

from src.utils.AsyncHelper import AsyncHelper


class TestAsyncHelper(TestCase):
    def test_run_multi_task(self):
        async def _slow_task():
            await asyncio.sleep(1)
            print('hello')

        l = []
        for i in range(5):
            l.append(_slow_task)
        AsyncHelper.run_multi_task(l)
