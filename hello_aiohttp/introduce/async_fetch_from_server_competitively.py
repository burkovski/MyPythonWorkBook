import time
import random
import asyncio
import aiohttp


URL = "https://api.github.com/events"
MAX_CLIENTS = 3


async def fetch_async(session, pid):
    start = time.time()
    delay = random.randint(2, 5)
    print("Fetch async {} started, delay for {} seconds.".format(pid, delay))
    await asyncio.sleep(delay)
    async with session.get(URL) as response:
        datetime = response.headers.get("Date")
    return "Process #{:<2}: {} took {:.2f} seconds".format(pid, datetime, time.time() - start)


async def asynchronous():
    start = time.time()
    async with aiohttp.ClientSession() as session:
        futures = [fetch_async(session, i) for i in range(1, MAX_CLIENTS + 1)]
        for (i, future) in enumerate(asyncio.as_completed(futures), start=1):
            result = await future
            print("{} {}".format(">>" * i, result))
    print("Process took: {:.2f} seconds".format(time.time() - start))


loop = asyncio.get_event_loop()
print("Process started!")
loop.run_until_complete(asynchronous())
loop.close()
