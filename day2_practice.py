import asyncio
import time
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv

from time_log import time_logger
load_dotenv()
print(f"加载到的 Key: {os.getenv('MY_LLM_KEY')}")

# 1. Type Hints & Pydantic 建模
class UserQuery(BaseModel):
    """定义用户请求模型"""
    query_id: int
    question: str = Field(..., min_length=2, description="用户提问内容")
    priority: Optional[int] = 1  # 可选字段，默认为 1
    timestamp: datetime = Field(default_factory=datetime.now)

class LLMResponse(BaseModel):
    """定义大模型响应模型"""
    answer: str
    processed_at: str
    latency: float

# 2. Asyncio 异步函数模拟 LLM 调用
@time_logger
async def mock_llm_call(query: UserQuery) -> LLMResponse:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 正在处理请求 #{query.query_id}: {query.question}...")

    start_time = time.perf_counter()
    try:
        # 模拟网络延迟（I/O 阻塞）
        await asyncio.sleep(2)
        answer = f"针对 '{query.question}' 的 AI 回答内容"
    except Exception as e:
        answer = f"请求 #{query.query_id} 调用失败：{e}"
    end_time = time.perf_counter()

    return LLMResponse(
        answer=answer,
        processed_at=datetime.now().isoformat(),
        latency=round(end_time - start_time, 2)
    )

# 3. 并发执行入口
async def main():
    # 准备测试数据
    queries = [
        UserQuery(query_id=1, question="什么是 MCP 协议？"),
        UserQuery(query_id=2, question="Python 异步编程怎么学？"),
        UserQuery(query_id=3, question="花生（猫）今天乖吗？") # 这里的“花生”是你的猫主子名
    ]

    print("--- 开始异步并发调用 ---")
    start_all = time.perf_counter()

    # 使用 asyncio.gather 同时发起所有请求
    tasks = [mock_llm_call(q) for q in queries]
    results: List[LLMResponse] = await asyncio.gather(*tasks)

    for res in results:
        print(f"响应结果: {res.answer} (耗时: {res.latency}s)")

    end_all = time.perf_counter()
    print(f"--- 全部处理完成，总耗时: {round(end_all - start_all, 2)}s ---")
    print("注意：虽然每个请求耗时 2s，但并发执行总耗时依然接近 2s！")

if __name__ == "__main__":
    asyncio.run(main())