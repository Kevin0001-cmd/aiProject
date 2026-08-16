# 流式接口
import anyio
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from openai import OpenAI
from pydantic import BaseModel

"""
启动命令：uvicorn main:app --reload --host 0.0.0.0 --port 8000
"""
app = FastAPI()

# client = OpenAI(
#     api_key="sk-xxx",  # 请替换为你的真实 Key
#     base_url="https://api.deepseek.com"
# )

# 模型名称填 "glm-4-flash"
client = OpenAI(
    api_key="xxx",
    base_url="https://open.bigmodel.cn/api/paas/v4"
)


class ChatRequest(BaseModel):
    messages: list[dict]
    stream: bool | None = True


# ✅ 1. 将同步的流式生成器包装为异步生成器
# ✅ 修复后的异步流式生成器
async def async_llm_stream(messages):
    # 在线程池中执行同步的 OpenAI SDK 调用
    stream = await anyio.to_thread.run_sync(
        lambda: client.chat.completions.create(
            model="glm-4-flash",
            messages=messages,
            stream=True
        )
    )

    iterator = iter(stream)
    while True:
        try:
            # 在线程池中获取下一个 chunk
            chunk = await anyio.to_thread.run_sync(next, iterator)
            yield chunk.model_dump_json()
        except StopIteration:
            # ✅ 核心修复：捕获生成器结束的信号，正常退出循环
            break
        except Exception as e:
            # 捕获其他可能的异常，防止流意外中断
            print(f"[服务端流式异常]: {e}")
            yield f'{{"error": "{str(e)}"}}'
            break


@app.post("/v1/chat/completions")
async def chat(req: ChatRequest):
    async def event_generator():
        try:
            # ✅ 2. 真正的边生成边发送
            async for chunk in async_llm_stream(req.messages):
                yield f"data: {chunk}\n\n".encode("utf-8")
            yield b"data: [DONE]\n\n"
        except Exception as e:
            print(f"[服务端流式异常]: {e}")
            yield f"data: {{\"error\": \"{str(e)}\"}}\n\n".encode("utf-8")

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )
