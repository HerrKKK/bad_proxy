import asyncio
import time


async def loop():
    while True:
        print('loop 1', time.time())
        await asyncio.sleep(2)
