from pydantic import BaseModel, ValidationError, Field
"""
核心属性：
以 Pydantic v2 为例：
e.errors()：返回错误列表，每条包含：type错误类型、loc出错字段路径、msg错误提示文本、input传入的原始输入值
e.json()：把错误序列化为 json 字符串，方便日志输出
e.title：异常标题
loc：嵌套字段会是数组，比如 ["user", "phone"] 代表 user 对象下 phone 字段错了
"""


"""
实践要点：
1. 不要依赖 msg 做业务判断：pydantic 版本升级文案会改动；判断逻辑用稳定的 type 字段。
2. 嵌套模型：loc 数组需要拼接成字段路径，".".join(map(str, err["loc"]))。
3. FastAPI：框架会自动捕获 ValidationError，包装成 HTTPValidationError 返回 400；自定义异常处理器可以重写返回格式。
4。错误类型全集：https://docs.pydantic.org.cn/latest/errors/validation_errors/ 全部 type 枚举，可用于翻译映射表。
"""

class ChatReq(BaseModel):
    query: str
    top_k: int = Field(ge=1, le=20)


bad_data = {"query": "", "top_k": 100}

try:
    req = ChatReq.model_validate(bad_data)
except ValidationError as e:
    # 1. 获取错误详情列表，最常用
    err_list = e.errors()
    print("=== errors() 得到list[dict] ===")
    for err in err_list:
        print(f"字段:{err['loc']}, 消息:{err['msg']}, 输入:{err['input']}")

    # 2. 输出为json字符串
    print("\n=== e.json() ===")
    print(e.json())

    # 3. 打印人类可读字符串
    print("\n=== str(e) ===")
    print(str(e))

