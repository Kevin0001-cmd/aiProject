# 模拟并发压测场景
# 10个协程各自做初始化，全部初始化完成，同一时刻发起请求

import asyncio

CONCURRENT = 10
barrier = asyncio.Barrier(parties=CONCURRENT)


async def request_sim(task_id):
    # 模拟每个协程做初始化、建立连接
    await asyncio.sleep(0.2)
    print(f"task {task_id}: 初始化完成，等待全部就绪")

    # 全部就绪后，才同时执行下面逻辑
    await barrier.wait()

    print(f"task {task_id}: ✅ 此刻同时发起请求")
    await asyncio.sleep(1)


async def main():
    coros = [request_sim(i) for i in range(CONCURRENT)]
    await asyncio.gather(*coros)


if __name__ == "__main__":
    asyncio.run(main())