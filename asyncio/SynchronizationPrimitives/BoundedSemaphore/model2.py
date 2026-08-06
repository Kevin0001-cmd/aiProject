import asyncio

MAX_CONCURRENT = 2
sem = asyncio.BoundedSemaphore(MAX_CONCURRENT)

async def task(n: int):
    await sem.acquire()
    try:
        print(f"task {n} running")
        await asyncio.sleep(1)
    finally:
        sem.release()  # 多调用一次这里就会抛 ValueError

async def main():
    coros = [task(i) for i in range(5)]
    await asyncio.gather(*coros)

if __name__ == "__main__":
    asyncio.run(main())