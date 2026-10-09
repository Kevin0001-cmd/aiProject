# Semaphore

import asyncio
import random
# 大量任务，限制最大并发 N，但是允许手动调用 `release()` 多次，把计数器超过初始 value
# 20个任务，只执行10个
# 哪个任务先结束，就立刻补上后面排队的任务；不是等整 10 个全部结束再开下一批。
# `gather + Semaphore`：**协程 Task 全部预先创建，运行时准入限流；不是延迟创建。**
# 如果任务数量非常巨大，优先 Queue + 固定 worker 池，避免一次性构造大量 Task。


MAX_CONCURRENT = 10
sem = asyncio.Semaphore(MAX_CONCURRENT)


async def task(i):
    async with sem:  # 自动 acquire + release
        t = random.uniform(0.5, 2.0)
        print(f"doing task {i}")
        await asyncio.sleep(t)
        print(f"finish task {i}")


async def main():
    total_tasks = 20
    # tips：会一次性创建出20个协程
    tasks = [task(i) for i in range(total_tasks)]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
