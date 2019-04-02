import asyncio


async def foo():                    # coroutine foo
    print("Running in foo")
    await asyncio.sleep(0)          # await - вернуть управление в event-loop
    print("Explicit context switch to foo again")


async def bar():                    # coroutine bar
    print("Explicit context to bar")
    await asyncio.sleep(0)          # async.sleep - неблокирующий вызов
    print("Implicit context switch back to bar")


ioloop = asyncio.get_event_loop()
tasks = [ioloop.create_task(foo()), ioloop.create_task(bar())]      # create_task - обрернуть coroutine в задачу
wait_tasks = asyncio.wait(tasks)                                    # объеденить задачи
ioloop.run_until_complete(wait_tasks)                               # выполнить запланированые задачи
ioloop.close()
