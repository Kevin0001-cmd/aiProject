import asyncio

MAX_CURRENT = 20
sem = asyncio.Semaphore(MAX_CURRENT)


# 分批次提交，不一次性gather全部，任务数量极大时，避免创建海量协程对象

async def worker(task_id: int):
    async with sem:
        print(f"[{task_id}] start")
        await asyncio.sleep(2)
        print(f"[{task_id}] done")


async def main():
    total = 30
    queue = asyncio.Queue()
    for i in range(total):
        await queue.put(i)

    async def consume():
        while not queue.empty():
            tid = await queue.get()
            await worker(tid)
            queue.task_done()

    consumers = [consume() for _ in range(MAX_CURRENT)]
    await asyncio.gather(*consumers)


if __name__ == "__main__":
    asyncio.run(main())
