import asyncio
# 开了8个消费者协程，但是BoundedSemaphore=3，实际最多同时运行 3 个任务。
MAX_CONCURRENT = 3
# 有界信号量，初始3，不允许release溢出
sem = asyncio.BoundedSemaphore(MAX_CONCURRENT)

async def task(n: int):
    async with sem:
        print(f"task {n} start")
        await asyncio.sleep(1.5)
        print(f"task {n} done")

async def main():
    tasks = [task(i) for i in range(8)]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())



