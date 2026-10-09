import asyncio
import time

async def say_after(delay, what):
    await asyncio.sleep(delay)
    return what

"""
一般**不要把同一个组的 task 又塞进 gather 里面**，二者都是等待原语，属于两套等待机制。

- `TaskGroup`：适合一组任务，fail‑fast，一个异常全部取消；离开 with 自动 await；用 `.result()` 获取返回。
- `asyncio.gather()`：手动等待一批 tasks；一个任务默认异常不会取消其他任务；直接返回结果列表。
"""
async def main():
    print(f"started at {time.strftime('%X')}")
    t1 = asyncio.create_task(say_after(1, 'hello'))
    t2 = asyncio.create_task(say_after(2, 'world'))
    res = await asyncio.gather(t1,t2)
    print(res)
    print(f"finished at {time.strftime('%X')}")

asyncio.run(main())
