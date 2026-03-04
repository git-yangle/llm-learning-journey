# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Personal 15-day learning journey for LLM application development and AI Coding. The repository evolves daily, progressing through Python fundamentals, MCP protocol, and ultimately building a full-stack LLM chat application.

## Learning Structure

- **Days 1–3**: Python modern features (Type Hints, asyncio, pydantic) + LLM API basics
- **Days 4–7**: Claude Code workflow + MCP (Model Context Protocol) custom server development
- **Days 8–14**: Full-stack LLM chat app (RAG, memory, SSE streaming, Streamlit/Gradio frontend)
- **Day 15**: Retrospective

Each day produces practice files named `dayN_*.py` (or similar), placed in `dayN/` subdirectory as content grows.

## Python 编码规范

### Type Hints（强制执行）

所有 Python 代码必须使用完整的 Type Hints，不允许裸写无类型的函数或变量：

```python
# ✅ 正确写法
from typing import Optional, List
from pydantic import BaseModel

async def chat(session_id: str, message: str) -> str:
    ...

# ❌ 禁止写法
async def chat(session_id, message):
    ...
```

- 函数参数、返回值必须标注类型
- 使用 `Optional[X]` 代替 `X | None`（保持与 Python 3.9 兼容）
- 集合类型使用 `typing` 模块：`List`, `Dict`, `Tuple`, `Set`

### Pydantic V2（数据模型首选）

所有数据模型统一使用 Pydantic V2，禁止使用 V1 兼容写法：

```python
# ✅ 正确写法（V2）
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    session_id: str
    message: str
    temperature: float = Field(default=0.7, ge=0.0, le=1.0)

# ❌ 禁止写法（V1 兼容层）
from pydantic import validator  # 用 field_validator 替代
```

### 异步规范

- 所有 LLM 调用必须使用 `AsyncAnthropic`，禁止使用同步客户端阻塞事件循环
- 并发任务使用 `asyncio.gather`，不要在 async 函数里调用 `time.sleep`

## 测试数据与占位符约定

项目中所有示例数据、占位符、测试用例统一使用以下约定：

| 占位符类型 | 固定值 |
|------------|--------|
| 示例用户名 | `peanut` |
| 示例 session_id | `peanut-session-001` |
| 示例宠物名 | `Peanut`（项目吉祥物，我的猫） |
| 测试问候语 | `"Hello, I'm Peanut!"` |

示例：

```python
# 单元测试示例
def test_chat_session():
    req = ChatRequest(session_id="peanut-session-001", message="Hello, I'm Peanut!")
    assert req.session_id == "peanut-session-001"
```

## 部署环境

### VPS 信息

| 项目 | 值 |
|------|-----|
| 域名 | `yanglemaodou.top` |
| 用途 | 生产部署 / API 对外暴露 |
| 部署方式 | 待定（预计 Docker + Nginx 反代） |

> 注意：VPS 相关的 SSH 密钥、密码等敏感信息不得出现在代码或注释中，统一通过环境变量或 `.env` 文件管理（已 gitignore）。

## Environment

- Python managed via **Miniconda**; activate the appropriate conda environment before running scripts.
- API keys stored in `.env` (gitignored); `ANTHROPIC_API_KEY` is read automatically by the Anthropic SDK, and `MY_LLM_KEY` is a custom alias loaded via `python-dotenv`.

## Running Scripts

```bash
# Run a day's practice script
python day2_practice.py
python day3/day3.py
python day3/day3_stream.py

# Run the FastAPI server (server.py)
uvicorn server:app --reload
```

## Architecture

### Current Files

| File | Role |
|------|------|
| `day2_practice.py` | Pydantic models + asyncio concurrent LLM mock calls; uses `@time_logger` decorator from `time_log.py` |
| `time_log.py` | Reusable async decorator `@time_logger` that wraps any async function and prints execution time |
| `day3/day3.py` | Interactive terminal chatbot with multi-turn conversation history using `AsyncAnthropic`; uses `claude-haiku-4-5-20251001` |
| `day3/day3_stream.py` | SSE streaming demo via `AsyncAnthropic` with `stream=True`; iterates `content_block_delta` events |
| `server.py` | FastAPI server with in-memory session management (`sessions` dict keyed by `session_id`); per-session `asyncio.Lock` prevents concurrent replies; `POST /chat`, `DELETE /chat/{session_id}` |

### Key Patterns

- All LLM calls use `AsyncAnthropic()` which reads `ANTHROPIC_API_KEY` from environment automatically.
- `server.py` holds conversation history in a plain dict — suitable for dev, not production.
- `time_log.py` exports a decorator intended to be applied with `@time_logger` on async functions.

## Key Technologies by Phase

| Phase | Stack |
|-------|-------|
| Python basics | `pydantic`, `asyncio`, `typing` |
| LLM API | Anthropic SDK (`anthropic`), token/temperature concepts |
| MCP | Python MCP SDK, custom MCP Server |
| Chat app backend | FastAPI + `AsyncAnthropic`, SSE streaming |
| Chat app frontend | Streamlit or Gradio |
| RAG | LangChain or LlamaIndex |
