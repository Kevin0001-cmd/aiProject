# 如何运行一个协程
# 并发执行
import asyncio
import time


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

"""
并发执行，main共花费2s
使用TaskGroup和create_task然后await最大的不同在于异常处理策略：
如果手动create_task然后await，要注意每一个task都要手动await，如果不await，就会变成孤儿任务，即使出错了也不会抛出。只有被await后，才会抛出错误。
使用TaskGroup，在with中是自动await所有任务的，而且，如果其中一个任务出错，所有的task都会被停止，抛出错误。

注意：asyncio是并发的，单线程时间循环，多个任务交替完成，宏观同时完成，不是并行的。
"""

async def main():
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(
            say_after(1, 'hello'))

        task2 = tg.create_task(
            say_after(2, 'world'))

        print(f"started at {time.strftime('%X')}")

    # 当上下文管理器退出时 await 是隐式执行的。

    print(f"finished at {time.strftime('%X')}")


asyncio.run(main())
