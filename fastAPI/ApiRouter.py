from fastapi import FastAPI, APIRouter

# 1. 创建主应用实例
app = FastAPI()

# 2. 创建路由实例
router = APIRouter(prefix="/items", tags=["items"])
routerb = APIRouter(prefix="/books", tags=["books"])


# 3. 在路由上定义接口
@router.get("/")
def list_items():
    return [{"id": 1, "name": "键盘"}]


@router.get("/list")
def list_items():
    return [{"id": 1, "name": "键盘"}]


@routerb.get("/")
def list_items():
    return [{"id": 1, "name": "键盘"}]


# 4. 【关键步骤】将路由注册到主应用中
app.include_router(router)
app.include_router(routerb)
