"""
## ✨小结 TaskGroup 两条铁律

1. 只要是`tg.create_task()`提交进去的任务，**无论你内部有没有 await 过，离开 async with 时，一定会全部等待完成才退出块**。
2. 组内任意任务发生异常 → TaskGroup 自动取消组内其余存活任务（fail‑fast 一损俱损）。

"""

import asyncio
import time


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(f"---- {what} done")
    return what

"""
场景：在 TaskGroup 的 with 内部只手动 await task1，不去 await task2；
离开 async with 的时候，TaskGroup 依然会隐式等待 task2，同时保留 fail‑fast 特性。
"""

async def main():
    print(f"main start: {time.strftime('%X')}")
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(say_after(1, 'hello'))
        task2 = tg.create_task(say_after(2, 'world'))

        print("inside with: before await task1")
        res1 = await task1  # 这里只等task1，此时task2还在后台sleep
        print(f"inside with: task1 finished, res1={res1}")
        # ⚠️ 注意：这里没有 await task2！

    # 退出async with块！TaskGroup自动等待剩下的task2完成
    print(f"out of with: {time.strftime('%X')}")
    res2 = task2.result()
    print(f"res2={res2}")


asyncio.run(main())
