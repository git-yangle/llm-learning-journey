import asyncio
import os
from anthropic import AsyncAnthropic


async def stream_claude_response():
    # 初始化异步客户端。它会自动寻找名为 ANTHROPIC_API_KEY 的环境变量
    client = AsyncAnthropic()

    print("🔌 正在与 Claude 建立长连接，等待首个 Token...")
    print("-" * 50)

    # 发起流式请求 (注意 stream=True 参数)
    stream = await client.messages.create(
        model="claude-3-haiku-20240307",  # 使用 Haiku 模型，响应速度最快，适合测试流式
        max_tokens=1024,
        temperature=0.5,
        system="你是一个资深的后端架构师。在回答时，请直接给出专业、落地的建议，拒绝废话。",
        messages=[
            {
                "role": "user",
                "content": "作为推荐系统的上游，我主要负责与推荐系统的数据交互，比如候选构建、特征获取以及 ua/ue 上报等。如果我想在现有的这些数据流转环节中引入大模型（LLM），你认为它可以解决哪些痛点？请给出两点简明的思路。",
            }
        ],
        stream=True,  # 开启 SSE 流式输出
    )

    # 异步迭代器：接收服务器推送过来的事件流
    async for event in stream:
        # 我们只需要提取文本增量块 (delta)
        if event.type == "content_block_delta":
            # end="" 确保不换行，flush=True 确保缓冲区的内容立刻打印到终端
            print(event.delta.text, end="", flush=True)

    print("\n" + "-" * 50)
    print("✅ 流式输出结束，连接已安全关闭！")


if __name__ == "__main__":

    # 启动异步事件循环
    asyncio.run(stream_claude_response())
