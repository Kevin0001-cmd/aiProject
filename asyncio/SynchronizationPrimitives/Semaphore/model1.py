# 固定消费者 + Queue（不需要 Semaphore）
# 并发 = 消费者数量，不需要 Semaphore。适合任务极多，不想一次性创建成千上百协程。
import asyncio
import queue

MAX_CONCURRENT = 10


async def worker(task_id: int):
    print(f"[{task_id}] start")
    await asyncio.sleep(2)
    print(f"[{task_id}] done")


async def consume():
    while True:
        # get 抛异常（被 cancel），不会走到 task_done，不会乱扣计数
        tid = await queue.get()
        try:
            await worker(tid)
        finally:
            # 内部维护一个未完成任务计数器，每次处理完一个item，调用queue.task_done()，计数器-1
            queue.task_done()


async def main():
    total = 30
    q = asyncio.Queue()  # 注意这里是协程队列，不是普通队列
    for i in range(total):
        await q.put(i)

    consumers = [consume() for _ in range(MAX_CONCURRENT)]
    # 阻塞主线程，直到计数器变成0，等待队列全部任务处理完成
    await q.join()

    # 全部任务做完，取消消费者协程
    for c in consumers:
        c.cancel()
    await asyncio.gather(*consumers, return_exceptions=True)


if __name__ == "__main__":
    asyncio.run(main())
