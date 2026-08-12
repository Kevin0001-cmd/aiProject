# routers/users.py
from fastapi import APIRouter

# 正确做法：创建插线板
router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
def get_users():
    return [{"id": 1, "name": "张三"}]