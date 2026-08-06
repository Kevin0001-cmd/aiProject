# Condition

import asyncio


async def consumer(cond: asyncio.Condition, queue: list):
    for _ in range(2):
        async with cond:
            # 条件不满足就一直等待，收到通知后还要再次判断条件（防止虚假唤醒）
            while not queue:
                print("消费者：队列为空，等待数据...")
                await cond.wait()

            # 拿到锁，条件满足，操作共享资源
            item = queue.pop(0)
            print(f"消费者：拿到数据 {item}")


async def producer(cond: asyncio.Condition, queue: list):
    for i in range(2):
        await asyncio.sleep(1)  # 模拟生产耗时
        async with cond:
            item = f"data-{i}"
            queue.append(item)
            print(f"生产者：生产 {item}，发送通知")
            cond.notify()  # 唤醒一个等待的协程


async def main():
    cond = asyncio.Condition()
    queue = []

    consumer_task = asyncio.create_task(consumer(cond, queue))
    producer_task = asyncio.create_task(producer(cond, queue))

    await asyncio.gather(consumer_task, producer_task)


asyncio.run(main())
