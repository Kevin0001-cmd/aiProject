import asyncio
"""
BoundedSemaphore能力 ≈ Semaphore，多了 release 溢出检测，发现 acquire/release 不成对直接抛异常，提早暴露 bug。
适合网络请求、爬虫等，希望并发数严格不能超标场景。
使用async with最安全，自动配对 acquire/release。
手动 release 务必放在finally，一旦漏 acquire 却调用 release，直接抛异常。
不要在同一个协程多次 acquire，会直接死锁。
"""
MAX_CONCURRENT = 3
sem = asyncio.BoundedSemaphore(MAX_CONCURRENT)


async def worker(task_id):
    async with sem:
        print(f"[{task_id}] work start")
        await asyncio.sleep(1)
        print(f"[{task_id}] work done")


async def consume(q: asyncio.Queue):
    while True:
        try:
            tid = await q.get()
        except asyncio.CancelledError:
            return
        try:
            await worker(tid)
        except Exception as e:
            print(f"err {tid}: {e}")
        finally:
            q.task_done()


async def main():
    q = asyncio.Queue()
    for i in range(10):
        await q.put(i)

    # 开5个消费者，但BoundedSemaphore限制最多同时3个执行
    consumers = [consume(q) for _ in range(5)]
    await q.join()

    for c in consumers:
        c.cancel()
    await asyncio.gather(*consumers, return_exceptions=True)


if __name__ == "__main__":
    asyncio.run(main())
