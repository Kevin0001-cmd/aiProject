from pydantic import ValidationError

from Pydantic.basicTypes import ChatReq


def parse_pydantic_validation_err(e: ValidationError) -> list[dict]:
    """将Pydantic ValidationError解析成对外可用错误列表"""
    result = []
    for err in e.errors():
        field_path = ".".join(map(str, err["loc"]))
        result.append({
            "field": field_path,
            "type": err["type"],
            "message": err["msg"],
        })
    return result

