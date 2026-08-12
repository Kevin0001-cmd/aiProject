# 异步路由

from fastapi import FastAPI
import asyncio

app = FastAPI()
"""
一句话总结：FastAPI 异步路由指async def定义的接口函数，
运行在 ASGI 事件循环；遇到await主动让出，
实现 IO 等待期间并发处理其他请求；
适合大模型流式 SSE；async def 
内部禁止直接调用同步阻塞代码。
"""


# 直接在ASGI事件循环主线程作为协程执行
@app.get("/async-demo")
async def async_demo():
    await asyncio.sleep(1)
    return {"msg": "异步路由完成"}


@app.get("/sync-demo")
def sync_demo():
    import time
    time.sleep(1)
    return {"msg": "同步路由完成"}
