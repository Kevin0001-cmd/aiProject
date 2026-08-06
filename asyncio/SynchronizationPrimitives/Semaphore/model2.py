# 生成很多任务，用 Semaphore 限流（不需要手动 Queue+consume）
# gather 大量协程 + Semaphore：协程全部预先创建，靠信号量控制并发。代码简洁，适合任务量中等。
import asyncio

MAX_CONCURRENT = 10
sem = asyncio.Semaphore(MAX_CONCURRENT)

async def worker(task_id: int):
    async with sem:
        print(f"[{task_id}] start")
        await asyncio.sleep(2)
        print(f"[{task_id}] done")

async def main():
    total = 30
    tasks = [worker(i) for i in range(total)]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())