"""
Day 10 — SSE 流式输出后端服务

核心知识点：
  SSE (Server-Sent Events) vs WebSocket
  ┌─────────────────┬─────────────────────────────┬──────────────────────────────┐
  │                 │ SSE                          │ WebSocket                    │
  ├─────────────────┼─────────────────────────────┼──────────────────────────────┤
  │ 方向            │ 单向（服务器 → 客户端）      │ 双向                         │
  │ 协议            │ HTTP/1.1                     │ WS（握手升级自 HTTP）         │
  │ 格式            │ text/event-stream            │ 自定义帧                     │
  │ 断线重连        │ 浏览器自动重连               │ 需手动实现                   │
  │ 适用场景        │ 通知推送、AI 流式回复        │ 游戏、实时协作               │
  └─────────────────┴─────────────────────────────┴──────────────────────────────┘

  SSE 协议格式（每条消息以两个换行结尾）：
    data: 消息内容\n\n
    event: 自定义事件名\n
    data: 消息内容\n\n
    id: 消息ID\n
    data: 消息内容\n\n
"""

import asyncio
import json

from anthropic import AsyncAnthropic
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

app = FastAPI(title="Day10 SSE 流式对话服务")

# 允许前端 HTML 文件（file://）跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = AsyncAnthropic()

# 用 session_id 隔离不同用户的对话历史，存在内存里
sessions: dict[str, list] = {}
locks: dict[str, asyncio.Lock] = {}


# ─────────────────────────────────────────
# 数据模型
# ─────────────────────────────────────────

class ChatRequest(BaseModel):
    session_id: str
    message: str


# ─────────────────────────────────────────
# 普通接口（对照用，一次性返回完整回复）
# ─────────────────────────────────────────

@app.post("/chat")
async def chat(req: ChatRequest):
    """非流式接口：等 AI 回复完整后一次性返回。"""
    lock = locks.setdefault(req.session_id, asyncio.Lock())
    if lock.locked():
        return {"error": "请等待上一条消息回复后再发送"}

    async with lock:
        history = sessions.setdefault(req.session_id, [])
        history.append({"role": "user", "content": req.message})

        response = await client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            system="你是一个资深的后端研发工程师，说话风格简洁、直击痛点。",
            messages=history,
        )

        reply = response.content[0].text
        history.append({"role": "assistant", "content": reply})

    return {"reply": reply}


# ─────────────────────────────────────────
# SSE 流式接口（核心）
# ─────────────────────────────────────────

async def sse_generator(session_id: str, message: str):
    """
    异步生成器：逐块 yield SSE 格式的数据。

    SSE 格式要求：
      - 每条消息必须以 "data: " 开头
      - 每条消息以 \n\n 结尾（两个换行），浏览器以此判断消息边界
      - 发送 [DONE] 作为流结束信号（约定俗成，参考 OpenAI 规范）
    """
    lock = locks.setdefault(session_id, asyncio.Lock())
    if lock.locked():
        # 用 SSE 格式返回错误，保持协议一致
        yield f"data: {json.dumps({'error': '请等待上一条消息回复后再发送'}, ensure_ascii=False)}\n\n"
        return

    async with lock:
        history = sessions.setdefault(session_id, [])
        history.append({"role": "user", "content": message})

        # 用 stream() 上下文管理器获取流式响应
        # SDK 内部将 HTTP 响应体作为异步迭代器暴露出来
        full_reply = ""
        async with client.messages.stream(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            system="你是一个资深的后端研发工程师，说话风格简洁、直击痛点。",
            messages=history,
        ) as stream:
            async for text_chunk in stream.text_stream:
                # text_chunk 是当前增量文本（可能是单个汉字，也可能是几个词）
                full_reply += text_chunk
                # 将增量文本序列化为 JSON，避免换行符破坏 SSE 格式
                yield f"data: {json.dumps({'delta': text_chunk}, ensure_ascii=False)}\n\n"

        # 流结束，保存完整回复到历史
        history.append({"role": "assistant", "content": full_reply})

    # 发送结束信号，前端收到后停止监听
    yield "data: [DONE]\n\n"


@app.get("/chat/stream")
async def chat_stream(
    session_id: str = Query(..., description="会话 ID"),
    message: str = Query(..., description="用户消息"),
):
    """
    SSE 流式接口。

    为什么用 GET 而不是 POST？
      浏览器原生的 EventSource API 只支持 GET 请求。
      如果必须用 POST（如传复杂 body），可改用 fetch() + ReadableStream 在前端手动解析。
      本示例优先展示 EventSource 原生用法，所以用 GET + Query 参数。
    """
    return StreamingResponse(
        sse_generator(session_id, message),
        # 必须设置 media_type，浏览器据此识别为 SSE 连接
        media_type="text/event-stream",
        headers={
            # 禁止缓存，确保每条消息实时到达
            "Cache-Control": "no-cache",
            # 保持连接，SSE 依赖长连接
            "Connection": "keep-alive",
            # 禁止 Nginx 等代理缓冲，否则会攒够一批再发
            "X-Accel-Buffering": "no",
        },
    )


# ─────────────────────────────────────────
# 会话管理
# ─────────────────────────────────────────

@app.delete("/chat/{session_id}")
async def clear_session(session_id: str):
    """清除指定会话的历史记录。"""
    sessions.pop(session_id, None)
    locks.pop(session_id, None)
    return {"ok": True}
