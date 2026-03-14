"""
Day 6: 自定义 MCP Server 实战
使用 FastMCP 实现 get_learning_progress 工具，读取 README.md 返回指定天的学习状态。
"""

import re
from pathlib import Path
from typing import Optional

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel


mcp = FastMCP("day6-learning-tracker")

# README.md 相对于此脚本的路径
README_PATH = Path(__file__).parent.parent / "README.md"


class LearningProgress(BaseModel):
    """某一天的学习进度信息"""
    day: int
    completed: bool
    description: Optional[str]
    message: str


@mcp.tool()
def get_learning_progress(day: int = 6) -> LearningProgress:
    """
    读取项目 README.md，返回指定天（默认 Day 6）的学习状态是否已完成。

    Args:
        day: 要查询的学习天数，默认为 6

    Returns:
        LearningProgress：包含完成状态和描述的结构化结果
    """
    if not README_PATH.exists():
        return LearningProgress(
            day=day,
            completed=False,
            description=None,
            message=f"README.md 未找到，路径：{README_PATH}",
        )

    content = README_PATH.read_text(encoding="utf-8")

    # 匹配形如 `- [x] **Day 6**：...` 或 `- [ ] **Day 6**：...` 的行
    pattern = re.compile(
        rf"- \[(?P<status>[x ])\] \*\*Day {day}\*\*[：:]\s*(?P<desc>.+)"
    )
    match = pattern.search(content)

    if not match:
        return LearningProgress(
            day=day,
            completed=False,
            description=None,
            message=f"README.md 中未找到 Day {day} 的记录",
        )

    completed = match.group("status") == "x"
    description = match.group("desc").strip()
    status_text = "✅ 已完成" if completed else "⬜ 未完成"

    return LearningProgress(
        day=day,
        completed=completed,
        description=description,
        message=f"Day {day} 学习状态：{status_text}\n内容：{description}",
    )


if __name__ == "__main__":
    mcp.run()
