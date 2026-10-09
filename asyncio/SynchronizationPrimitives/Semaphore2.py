import asyncio

MAX_CURRENT = 20


# 分批次提交，不一次性gather全部，任务数量极大时，避免创建海量协程对象
# tips：不会一次性创建出大量协程

async def worker(task_id: int):
    print(f"[{task_id}] start")
    await asyncio.sleep(2)
    print(f"[{task_id}] done")


async def consume(queue: asyncio.Queue):
    while True:
        tid = await queue.get()
        if tid is None:
            queue.task_done()
            break
        try:
            await worker(tid)
        finally:
            queue.task_done()


async def main():
    total = 30
    queue = asyncio.Queue()
    for i in range(total):
        await queue.put(i)

    for _ in range(MAX_CURRENT):
        await queue.put(None)

    consumers = [consume(queue) for _ in range(MAX_CURRENT)]
    await asyncio.gather(*consumers)


if __name__ == "__main__":
    asyncio.run(main())

"""
# asyncio.Queue 哨兵模式
## put追加到队尾 FIFO
哨兵None追加全部业务任务之后，队列顺序：[业务items..., None, None ...]

## 哨兵含义
None是一个约定好的特殊标记（哨兵），worker读到哨兵就主动break循环退出。
⚠️规则：
1. put哨兵的个数 == worker协程的个数；
2. 哨兵也是队列item，拿到之后也必须调用 task_done();
3. 不需要join之后手动cancel协程，worker自己退出。

## task_done()
Queue内部维护未完成计数器：
put() → +1； task_done() →‑1；
queue.join()阻塞直到计数器等于0。
task_done()不删除队列元素，只是修改计数。

"""