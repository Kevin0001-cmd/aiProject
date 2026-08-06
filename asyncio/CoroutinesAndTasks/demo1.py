# 如何运行一个协程
import asyncio
import time

# 机制一
async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

# 链式调用
async def main():
    print(f"started at {time.strftime('%X')}")

    await say_after(1,'hello')
    await say_after(2,'world')

    print(f"finished at {time.strftime('%X')}")

asyncio.run(main())