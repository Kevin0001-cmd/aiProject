import asyncio

async def main():
    print("Hello ...")
    await asyncio.sleep(2)
    print("... World!")

# asyncio.run(main())

# 简单的调用一个协程不会使其被调度执行
# if __name__ == '__main__':
#     main()