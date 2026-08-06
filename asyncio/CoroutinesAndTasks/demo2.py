# 如何运行一个协程
# 并发运行
import asyncio
import time


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

# 并发执行，不是任务链式调用
async def main():
    task1 = asyncio.create_task(say_after(1, 'hello'))
    task2 = asyncio.create_task(say_after(2, 'world'))

    print(f"started at {time.strftime('%X')}")

    await task1
    await task2

    print(f"finished at {time.strftime('%X')}")


asyncio.run(main())
