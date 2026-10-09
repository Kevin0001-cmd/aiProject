# 如何运行一个协程
# 并发执行
# 可与demo5.py对比
import asyncio
import time


async def say_after(delay, what):
    await asyncio.sleep(delay)
    # print(what)
    return what


async def main():
    print(f"started at {time.strftime('%X')}")
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(
            say_after(1, 'hello'))

        task2 = tg.create_task(
            say_after(2, 'world'))

    # results = await asyncio.gather(task1, task2)
    results = [task1.result(), task2.result()]
    print(results)
    # 当上下文管理器退出时 await 是隐式执行的。
    print(f"finished at {time.strftime('%X')}")


asyncio.run(main())
