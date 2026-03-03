import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
from anthropic import AsyncAnthropic

app = FastAPI()
client = AsyncAnthropic()

# 用 session_id 隔离不同用户的对话历史，存在内存里
# 生产环境应换成 Redis 或数据库
sessions: dict[str, list] = {}
locks: dict[str, asyncio.Lock] = {}


class ChatRequest(BaseModel):
    session_id: str   # 小程序端生成，用来标识哪个用户/哪轮会话
    message: str


@app.post("/chat")
async def chat(req: ChatRequest):
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


@app.delete("/chat/{session_id}")
async def clear_session(session_id: str):
    sessions.pop(session_id, None)
    return {"ok": True}
