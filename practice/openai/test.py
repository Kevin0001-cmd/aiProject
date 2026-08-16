import json
import requests
from requests.exceptions import ChunkedEncodingError, Timeout

if __name__ == "__main__":
    try:
        resp = requests.post(
            "http://localhost:8000/v1/chat/completions",
            json={
                "messages": [{"role": "user", "content": "我最近想从南京出发，去另外的地方，进行一个周末游，预算是1000元，我的目的是欣赏美丽的风景，这1000元中包含车票、住宿、饮食，请帮我写一份旅行计划。推荐地点并列出当地可游玩的地点。"}],
                "stream": True
            },
            stream=True,
            timeout=(10, 60),
            proxies={"http": None, "https": None}
        )
        resp.raise_for_status()

        for line in resp.iter_lines():
            if line:
                text = line.decode("utf-8")
                if text.startswith("data:"):
                    payload = text[5:].strip()
                    if payload == "[DONE]":
                        print("\n[流式输出结束]")
                        break
                    # ✅ 核心修改：解析 JSON，只提取 content 字段
                    try:
                        chunk = json.loads(payload)
                        content = chunk.get("choices", [{}])[0].get("delta", {}).get("content", "")
                        if content:
                            print(content, end="", flush=True)
                    except json.JSONDecodeError:
                        print(f"\n[解析异常]: {payload}", end="", flush=True)

    except ChunkedEncodingError as e:
        print(f"\n[警告] 流式传输中断: {e}")
    except Timeout as e:
        print(f"\n[警告] 请求超时: {e}")
    except Exception as e:
        print(f"\n[错误] 发生未知异常: {e}")