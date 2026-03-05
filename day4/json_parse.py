import json
from typing import Any, Optional, Union


def parse_json(raw: str) -> Optional[Any]:
    """
    解析 JSON 字符串，返回对应的 Python 对象。
    解析失败时返回 None。
    """
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


def parse_json_strict(raw: str) -> Any:
    """
    严格模式解析 JSON 字符串，解析失败时抛出 ValueError。
    """
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON 解析失败：{e}") from e


def get_nested(data: Any, *keys: Union[str, int], default: Any = None) -> Any:
    """
    从嵌套的 dict/list 中安全读取值。
    支持字符串键（dict）和整数索引（list）混合路径。

    示例：
        get_nested(data, "user", "name")
        get_nested(data, "items", 0, "id")
    """
    current = data
    for key in keys:
        try:
            current = current[key]
        except (KeyError, IndexError, TypeError):
            return default
    return current


if __name__ == "__main__":
    # 基本解析
    raw_valid = '{"name": "Peanut", "age": 3, "tags": ["cat", "cute"]}'
    result = parse_json(raw_valid)
    print("解析结果：", result)

    # 嵌套读取
    nested_json = '{"user": {"name": "peanut", "scores": [95, 87, 100]}}'
    data = parse_json(nested_json)
    name = get_nested(data, "user", "name")
    first_score = get_nested(data, "user", "scores", 0)
    missing = get_nested(data, "user", "email", default="未设置")
    print("用户名：", name)
    print("第一个分数：", first_score)
    print("邮箱（缺省）：", missing)

    # 无效 JSON
    raw_invalid = '{name: Peanut}'
    print("无效 JSON 结果：", parse_json(raw_invalid))

    # 严格模式
    try:
        parse_json_strict(raw_invalid)
    except ValueError as e:
        print("严格模式捕获异常：", e)
