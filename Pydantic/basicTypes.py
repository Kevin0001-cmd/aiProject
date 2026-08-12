"""
基础类型
"""
from typing import Literal
"""
EmailStr,        # 邮箱校验：pip install pydantic[email]
AnyHttpUrl,      # http/https url校验
SecretStr,       # 密码，打印时隐藏为***
UUID4            # uuid格式校验
"""
from pydantic import BaseModel, Field, EmailStr, AnyHttpUrl, SecretStr
from datetime import datetime


class User(BaseModel):
    id: int
    name: str
    money: float
    is_active: bool
    created_at: datetime | None = None
    tags: list[str]  # 字符串列表
    meta: dict[str, str]  # key字符串，value数字的字典
    ids: set[int]  # int集合，自动去重
    mode: Literal["user", "admin"]  # 只能是指定字面量


class ChatReq(BaseModel):
    # ge >= ; gt > ; le <= ; lt <
    top_k: int = Field(default=5, ge=1, le=20)
    prompt: str = Field(min_length=1, max_length=2000)


# 嵌套Model
class Message(BaseModel):
    role: Literal["user","assistant"]
    content: str

class ChatRequest(BaseModel):
    query: str
    history: list[Message]  # 嵌套模型列表

