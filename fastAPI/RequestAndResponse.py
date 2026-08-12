# 请求拦截与响应过滤

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class UserIn(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str


@app.post("/users/", response_model=UserOut)
def create_user(u: UserIn):
    return {"id": 1, "username": u.username, "password": u.password}
