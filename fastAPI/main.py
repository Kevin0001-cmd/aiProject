from fastapi import FastAPI
from pydantic import BaseModel
"""
启动命令
在cmd中激活ai_agent环境，cd到当前目录下，执行
(ai_agent) D:\2_project\zkf_python\aiProject\fastAPI>python -m fastapi dev main.py

访问地址
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc
"""
app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.price, "item_id": item_id}

