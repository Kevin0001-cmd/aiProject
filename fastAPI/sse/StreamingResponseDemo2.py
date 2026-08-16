import anyio
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()


async def sse_generator():
    for i in range(10):
        # SSE 固定格式：data:内容\n\n
        msg = f"data: some fake video bytes xixi 第{i + 1}条\n\n"
        yield msg.encode("utf-8")
        await anyio.sleep(0.5)


"""
流式输出
"""


@app.get("/stream")
async def stream_demo():
    return StreamingResponse(
        sse_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Content-Type-Options": "nosniff"
        }
    )
