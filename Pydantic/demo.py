"""
pydantic的基本使用
"""

from pydantic import BaseModel, Field
from datetime import datetime

"""
email: str | None = None
为什么这么写？
str | None：允许这个字段的值是字符串 或者 None（类型层面放开）
= None：用户不提供该字段时，自动给它填 None（默认值）
"""


class User(BaseModel):
    id: int
    name: str
    email: str | None = None


class ChatRequest(BaseModel):
    query: str  # 普通字符串
    temperature: float = 0.7  # 带默认值
    top_k: int = Field(default=5, ge=1, le=20)  # 数字范围校验 1~20
    history: list[str] = []  # 列表
    create_time: datetime | None = None


u = User(id="123", name="zhangsan", email="xxx@163.com")
print(u.id)
d = u.model_dump()
print(d)
# {'id': 123, 'name': 'zhangsan', 'email': 'xxx@163.com'}
print(type(d))  # dict，可以做字典操作：d["id"]、修改d['name']

s = u.model_dump_json()
print(s)
# {"id":123,"name":"zhangsan","email":"xxx@163.com"}
print(type(s))  # str，只是一长串文本字符串，不能 s["id"]

print("--------------------------------------------")
req = ChatRequest(query="hi", create_time=datetime(2026, 8, 6))

d = req.model_dump()
print(d["create_time"], type(d["create_time"]))
# 2026‑08‑06 00:00:00 <class 'datetime.datetime'>

s = req.model_dump_json()
print(s)
# {"query":"hi","temperature":0.7,"top_k":5,"history":[],"create_time":"2026‑08‑06T00:00:00"}
