from pydantic import BaseModel, ValidationError

class User(BaseModel):
    phone: str

try:
    User(phone=1)
except ValidationError as e:
    err_list = e.errors()
    # 提取字段+提示，用于接口返回 / excel报错
    for err in err_list:
        field = ".".join(map(str, err["loc"]))
        msg = err["msg"]
        print(f"字段:{field}, 原因:{msg}")