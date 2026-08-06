import asyncio

barrier = asyncio.Barrier(parties=4)


async def worker(name: str):
    print(f"{name}正在做前置准备")
    await asyncio.sleep(1)

    print(f"{name}到达栅栏，等待其他伙伴...")
    # 在这里阻塞，凑齐4个协程才往下走
    await barrier.wait()

    # 全部放行后，同时执行下面的代码
    print(f"{name}=====> 统一开始执行业务！")


async def main():
    tasks = [worker(f"task-{i}") for i in range(4)]
    await asyncio.gather(*tasks)
    print("全部完成")


if __name__ == '__main__':
    asyncio.run(main())
