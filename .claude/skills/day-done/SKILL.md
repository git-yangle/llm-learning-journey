---
name: day-done
description: “Day X 完成”、”提交今天的进度”时，执行学习结束工作流。不适用于普通 git 提交场景。
version: 1.1.0
user-invocable: true
disable-model-invocation: true
argument-hint: [day-number] [commit-message]
allowed-tools: Bash(git:*), Read, Edit, mcp__study-commit__get_git_commit_info, mcp__study-commit__py_file_check
---

## 参数说明

- `$ARG1`：天数（如 `7`），用于更新 README.md 中的完成标记
- `$ARG2`：提交信息（如 `day 7 complete: MCP Server 开发实战`）

## 当前状态

当前分支: !`git branch --show-current`

## 执行步骤

1. 检查参数：若 `$ARG1` 或 `$ARG2` 为空，提示用法 `/day-done [天数] [提交信息]`，终止执行
2. 调用 mcp study-commit（`get_git_commit_info`）获取当前项目 git 信息；若无任何文件变更，提示”无内容可提交”，终止执行
3. 更新 README.md：将 `- [ ] **Day $ARG1**` 替换为 `- [x] **Day $ARG1**`；若找不到对应行，提示用户手动确认后继续
4. 展示 study-commit 返回的当前变更信息（git status + git diff），等待用户回复”确认”或”ok”后继续
5. 调用 mcp study-commit（`py_file_check`）对本次变更中的 `.py` 文件逐一进行语法检查；若有编译错误，展示错误信息，终止执行；否则继续
6. 执行：`git add -A` → `git commit -m “$ARG2”`
7. 告知 commit 完成，**提示用户手动执行 `git push`**，不自动 push

## 禁止行为

- 不得自动执行 `git push`，必须由用户手动触发（遵守 CLAUDE.md 规定）
- 不得修改 README.md 以外的文件内容

