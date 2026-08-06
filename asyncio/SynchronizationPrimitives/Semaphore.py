# Semaphore

import asyncio
# 大量任务，限制最大并发 N
# 20个任务，只执行10个

MAX_CONCURRENT = 10
sem = asyncio.Semaphore(MAX_CONCURRENT)


async def task(i):
    async with sem:  # 自动 acquire + release
        print(f"doing task {i}")
        await asyncio.sleep(2)
        print(f"finish task {i}")


async def main():
    total_tasks = 20
    tasks = [task(i) for i in range(total_tasks)]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
