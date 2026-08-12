# main.py
from fastapi import FastAPI
from routers.users import router as users_router  # ← 改这里


app = FastAPI()  # 唯一的主机

# 把插线板插到主机上
app.include_router(users_router)
