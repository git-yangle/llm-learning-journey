---
name: py-conventions
description: 当遇到"写一个 Python 函数"、"定义一个类"、"写异步代码"、"用 Pydantic 建模"、"加类型标注"、"调用 Anthropic API"、"实现 LLM 调用"时这些行为时，自动加载此 skill 作为编码规范参考。不适用于纯理论问题或 Go/TypeScript 等非 Python 场景。
version: 1.0.0
user-invocable: false
---

# Python 编码规范（本项目）

本项目的 Python 编码约定，所有代码输出必须严格遵守以下规范。

## Type Hints（强制）

所有函数参数和返回值必须标注类型，无例外：

```python
# ✅ 正确
from typing import Optional, List, Dict
async def chat(session_id: str, message: str) -> str: ...
def parse_items(data: List[Dict[str, str]]) -> Optional[str]: ...

# ❌ 禁止
async def chat(session_id, message): ...
```

- 用 `Optional[X]` 代替 `X | None`（保持 Python 3.9 兼容）
- 集合类型统一用 `typing` 模块：`List`、`Dict`、`Tuple`、`Set`

## Pydantic V2（数据模型首选）

统一使用 Pydantic V2，禁止 V1 兼容写法：

```python
# ✅ 正确（V2）
from pydantic import BaseModel, Field, field_validator

class ChatRequest(BaseModel):
    session_id: str
    message: str
    temperature: float = Field(default=0.7, ge=0.0, le=1.0)

# ❌ 禁止（V1 兼容层）
from pydantic import validator  # 改用 field_validator
```

## 异步规范

- LLM 调用必须用 `AsyncAnthropic`，禁止同步客户端阻塞事件循环
- 并发任务用 `asyncio.gather`，禁止在 async 函数中调用 `time.sleep`

```python
# ✅ 正确
from anthropic import AsyncAnthropic
client = AsyncAnthropic()

# ❌ 禁止
from anthropic import Anthropic  # 同步客户端
```

## 代码注释

- 注释统一使用**中文**

## Claude 的行为要求

- 输出所有 Python 代码时，自动遵守上述规范，无需用户提醒
- 若检测到用户提供的代码违反上述规范，在回复前先指出违规点并给出修正版本
- 若用户明确要求豁免某条规范，可豁免但需在回复中说明理由


