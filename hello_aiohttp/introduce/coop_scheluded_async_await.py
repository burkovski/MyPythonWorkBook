import asyncio
import time


def timer(start):
    def tic():
        return time.time() - start
    return tic


async def task1(tic):
    print("task #1 started work: {:.1f}".format(tic()))
    await asyncio.sleep(2)      # имитация длительного процесса(I/O)
    print("task #1 ended work: {:.1f}".format(tic()))


async def task2(tic):
    print("task #2 started work: {:.1f}".format(tic()))
    await asyncio.sleep(2)
    print("task #2 ended work: {:.1f}".format(tic()))


async def task3(tic):
    print("Let's do some stuff while the coroutines are blocked, {:.1f}".format(tic()))
    await asyncio.sleep(1)      # пока две предыдущие функции ждут окончания I/O, эта функция может поработать
    print("Done!")


tic_func = timer(time.time())
ioloop = asyncio.get_event_loop()
tasks = [
    ioloop.create_task(task1(tic_func)),
    ioloop.create_task(task2(tic_func)),
    ioloop.create_task(task3(tic_func))
]
ioloop.run_until_complete(asyncio.wait(tasks))
ioloop.close()
