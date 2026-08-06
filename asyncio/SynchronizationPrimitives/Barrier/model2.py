# 协程数量 > parties，演示多次轮回
"""
Barrier是可复用的，放行之后重置，可以第二轮继续等待。
这里 parties=2，一共启动 4 个协程，分两批放行。
"""

import asyncio

barrier = asyncio.Barrier(parties=2)


async def worker(name):
    for round_num in range(2):
        print(f"{name} round{round_num}: 准备完毕，等待栅栏")
        await barrier.wait()
        print(f"{name} round{round_num}: 开始运行")
        await asyncio.sleep(0.5)


async def main():
    tasks = [worker(f"w{i}") for i in range(4)]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
