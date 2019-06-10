import time
import urllib.request
import asyncio
import aiohttp


URL = "https://api.github.com/events"
MAX_CLIENTS = 10


def fetch_sync(pid):
    print("Fetch sync process #{:<2} started.".format(pid))
    start = time.time()
    response = urllib.request.urlopen(URL)      # блокирующий запрос
    datetime = response.getheader("Date")
    print("Process #{:<2}: {}, took: {:.2f} seconds".format(
        pid, datetime, time.time() - start
    ))
    return datetime


async def fetch_async(session, pid):
    print("Fetch async process #{:<2} started.".format(pid))
    start = time.time()
    async with await session.get(URL) as response:   # что такое блокирование?
        datetime = response.headers.get("Date")
    print("Process #{:<2}: {}, took: {:.2f} seconds".format(
        pid, datetime, time.time() - start
    ))
    return datetime


def synchronous():
    start = time.time()
    for i in range(1, MAX_CLIENTS + 1):
        fetch_sync(i)
    print("Responses took: {:.2f} seconds".format(time.time() - start))


async def asynchronous():
    start = time.time()
    async with aiohttp.ClientSession() as session:      # сессия асихронного HTTP-запроса
        tasks = [asyncio.ensure_future(fetch_async(session, i))
                 for i in range(1, MAX_CLIENTS + 1)]
        await asyncio.wait(tasks)
    print("Process took: {:.2f} seconds".format(time.time() - start))


print("Synchronous:")
synchronous()


print("\nAsynchronous:")
loop = asyncio.get_event_loop()
loop.run_until_complete(asynchronous())
loop.close()
