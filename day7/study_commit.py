import logging
import py_compile
import subprocess
from mcp.server.fastmcp import FastMCP
from typing import Any, Optional, List
from starlette.requests import Request
from starlette.responses import Response
from pydantic import BaseModel, Field
from starlette.middleware.base import BaseHTTPMiddleware
import uvicorn

# 统一日志配置
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


class PyBuilderChecker(BaseModel):
    """py检查结果"""

    success: bool
    err_info: Optional[str] = Field(default=None, description="检查的错误信息")


class GitLogRecent(BaseModel):
    """最近的git信息"""

    last_commit: Optional[List[str]] = Field(..., description="最近的5条git log")
    git_status_res: str = Field(..., description="git status 的结果")
    git_diff_res: Optional[str] = Field(default=None, description="git diff --name-only")


class BearerAuthMiddleware(BaseHTTPMiddleware):
    """验证请求头中的 Bearer Token"""

    async def dispatch(self, request: Request, call_next: Any) -> Response:
        token = "1234"
        auth_header = request.headers.get("Authorization", "")
        if not token or auth_header != f"Bearer {token}":
            return Response("Unauthorized", status_code=401)
        return await call_next(request)


mcp = FastMCP("commit-checker-http", stateless_http=True)


@mcp.tool()
def get_git_commit_info(path_file: str) -> GitLogRecent:
    """
    读取指定项目目录下最近的git提交信息。执行`git log --oneline -5`、`git status` 和 `git diff --name-only`

    Args:
        path_file: 项目的路径

    Returns:
        GitLogRecent: 最近的git提交信息，last_commit 对应 git log --oneline -5，
                      git_status_res 对应 git status，git_diff_res 对应 git diff --name-only。
                      各命令失败时对应字段返回错误描述。
    """
    rtn = GitLogRecent(last_commit=[], git_status_res="")

    try:
        result_log = subprocess.run(
            ["git", "log", "--oneline", "-5"],
            capture_output=True,
            text=True,
            cwd=path_file,
        )
        if result_log.returncode == 0:
            rtn.last_commit.append(result_log.stdout)
        else:
            rtn.last_commit = None
            logger.error("git log 执行失败: %s", result_log.stderr)
    except Exception as e:
        rtn.last_commit = None
        logger.error("git log 异常: %s", e)

    try:
        result_status = subprocess.run(
            ["git", "status"],
            capture_output=True,
            text=True,
            cwd=path_file,
        )
        if result_status.returncode == 0:
            rtn.git_status_res = result_status.stdout
        else:
            rtn.git_status_res = "执行失败"
            logger.error("git status 执行失败: %s", result_status.stderr)
    except Exception as e:
        rtn.git_status_res = "执行失败"
        logger.error("git status 异常: %s", e)

    try:
        result_diff = subprocess.run(
            ["git", "diff", "--name-only"],
            capture_output=True,
            text=True,
            cwd=path_file,
        )
        if result_diff.returncode == 0:
            rtn.git_diff_res = result_diff.stdout
        else:
            logger.error("git diff 执行失败: %s", result_diff.stderr)
    except Exception as e:
        logger.error("git diff 异常: %s", e)

    return rtn


@mcp.tool()
def py_file_check(path_file: str) -> PyBuilderChecker:
    """
    编译指定python文件，对语法进行检查

    Args:
        path_file: 需要检查的对应路径的文件名

    Returns:
        PyBuilderChecker: 检查是否通过，以及失败的错误信息
    """
    try:
        py_compile.compile(path_file, doraise=True)
        logger.info("语法检查通过: %s", path_file)
        return PyBuilderChecker(success=True)
    except py_compile.PyCompileError as e:
        logger.warning("语法检查失败: %s", e)
        return PyBuilderChecker(success=False, err_info=f"语法错误: {e}")


if __name__ == "__main__":
    app = mcp.streamable_http_app()
    app.add_middleware(BearerAuthMiddleware)
    uvicorn.run(app, host="127.0.0.1", port=8766)
