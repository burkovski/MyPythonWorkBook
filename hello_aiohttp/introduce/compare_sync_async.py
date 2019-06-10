import random
import asyncio
import time


def task(pid):      # "скучная" синхронщина
    delay = random.randint(0, 5) * 0.1
    time.sleep(delay)
    print("Task {:2} done after {:.1f}!".format(pid, delay))


async def task_coroutine(pid):
    delay = random.randint(0, 5) * 0.1
    await asyncio.sleep(delay)              # неблокирующий вызов
    print("Task {:2} done after {:.1f}!".format(pid, delay))


def synchronous():
    for i in range(1, 10):
        task(i)


async def asynchronous():
    # обернуть coroutines -> получить futures
    tasks = [asyncio.ensure_future(task_coroutine(i)) for i in range(1, 10)]
    await asyncio.wait(tasks)


start = time.time()
print("Synchronous:")
synchronous()
print("Total time: {:.1f}".format(time.time() - start))


ioloop = asyncio.get_event_loop()
start  = time.time()
print("\nAsynchronous:")            # ну и кто здесь победитель?!
ioloop.run_until_complete(asynchronous())
print("Total time: {:.1f}".format(time.time() - start))
ioloop.close()
