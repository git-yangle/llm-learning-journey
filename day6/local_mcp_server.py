from mcp.server.fastmcp import FastMCP
from typing import Any, Optional, Union
import glob
import linecache
from pydantic import BaseModel



class LogFileResut(BaseModel):
    line: int
    content: str


class LogFileList(BaseModel):
    files: list[str]


mcp = FastMCP("learning-tracker")


@mcp.tool()
def list_log_files(path: str) -> LogFileList:
    """
    读取系统指定路径下的所有.log文件名列表。

    Args:
        path: 要查询的路径

    Returns:
        LogFileList: 包含所有.log文件名的列表结果
    """
    glob_files = glob.glob(f"{path}/**/*.log", recursive=True)
    return LogFileList(files=glob_files)


@mcp.tool()
def read_log_file(file_name: str, line_number: int) -> LogFileResut:
    """
    读取系统指定路径下文件名对应的指定行内容。

    Args:
        file_name: 要查询的文件名
        line_number: 要查询的行号

    Returns:
        LogFileResut: 读取系统指定路径下文件名对应的指定行的字符串输出
    """
    content = linecache.getline(file_name, line_number)
    return LogFileResut(line=line_number, content=content)


if __name__ == "__main__":
    mcp.run()
