# Condition

import asyncio

"""
## 📌总结思考要点
1. ✅生产者可以先批量 append 多条任务，**最后调用 notify_all () 一次性唤醒全部等待的消费者**。
2. `notify_all()`只是唤醒；唤醒后所有 consumer 仍然竞争 Condition 底层锁；同一时刻只有一个 consumer 操作共享 list。
3. **while 循环判断条件必须保留！**
   - 场景：notify_all 唤醒 2 个 consumer；第一个 consumer 拿到锁把队列全部任务 pop 完；第二个 consumer 拿到锁发现 queue 又空，继续 wait。
4. ❗业务 IO、sleep**一定要移出 `async with cond:` 锁块**；临界区只做 append/pop；尽快释放锁。
5. 对比 asyncio.Queue：
   - Condition+list 是自己手动实现生产者消费者；自己管理 notify；
   - asyncio.Queue 内部本身就是基于 Condition 封装好的，不用手动 notify。
"""

async def consumer(cond: asyncio.Condition, queue: list):
    for _ in range(2):
        async with cond: # 当前已经持有锁！
            # 条件不满足就一直等待，收到通知后还要再次判断条件（防止虚假唤醒）
            while not queue:
                print("消费者：队列为空，等待数据...")
                # 自动释放底层锁；被唤醒之后重新竞争拿到锁，函数返回。
                # 返回之后仍然处于async with锁保护区内；读取共享变量是线程安全。
                await cond.wait()

            # 拿到锁，条件满足，操作共享资源
            item = queue.pop(0)
        print(f"消费者：拿到数据 {item}")

# 往队列里面放入一个item，然后用cond唤醒一个等待线程
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
