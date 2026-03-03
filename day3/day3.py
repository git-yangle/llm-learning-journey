import asyncio
from anthropic import AsyncAnthropic
from pydantic import BaseModel, Field


client = AsyncAnthropic()

async def chat():
    messages = []
    is_waiting = False
    loop = asyncio.get_event_loop()
    print("开始对话（输入 'exit' 退出）\n")

    while True:
        user_input = (await loop.run_in_executor(None, input, "你: ")).strip()
        if user_input.lower() == "exit":
            print("再见！")
            break
        if not user_input:
            continue
        if is_waiting:
            print("请等待上一条消息回复后再发送\n")
            continue

        messages.append({"role": "user", "content": user_input})
        is_waiting = True
        print("Claude 思考中...\n")

        response = await client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            system="你是一个资深的后端研发工程师，说话风格简洁、直击痛点。",
            messages=messages,
        )

        reply = response.content[0].text
        messages.append({"role": "assistant", "content": reply})
        is_waiting = False

        print(f"Claude: {reply}\n")



# 定义数据模型
class UserInfo(BaseModel):
    id: int
    name: str
    age: int = Field(default=18, ge=0)  # 默认 18 岁，且必须大于等于 0

# 假设这是大模型返回的 JSON 字典
mock_json_from_llm = {
    "id": "1001",  # Pydantic 会自动把字符串 "1001" 转成整型 1001
    "name": "Peanut"
}

# 实例化并自动校验
user = UserInfo(**mock_json_from_llm)
print(user.id, type(user.id)) 
 # 打印: 1001 <class 'int'>
if __name__ == "__main__":
    asyncio.run(chat())
