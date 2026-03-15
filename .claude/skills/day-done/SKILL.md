---
name: day-done
description: ”Day X 完成”、”提交今天的进度”时，执行学习结束工作流。不适用于普通 git 提交场景。
version: 1.0.0
user-invocable: true
disable-model-invocation: true
argument-hint: [day-number] [commit-message]
allowed-tools: Bash(git:*), Read, Edit
---

## 当前状态
当前分支: !`git branch --show-current`
通过mcp study-commit 来获取当前项目的git信息

## 执行步骤

1. 检查参数：若 $ARGUMENTS 为空，提示用法 `/day-done [天数] [提交信息]`，终止执行
2. 若当前项目的git信息无任何文件变更，提示”无内容可提交”，终止执行
3. 更新 README.md：将 `- [ ] **Day $0**` 替换为 `- [x] **Day $1**`；
4. 展示study-commit返回的当前变更信息，等待用户回复”确认”或”ok”后继续
5. 执行：`git add -A` → `git commit -m “$1”`
6. 告知 commit 完成，**提示用户手动执行 `git push`**，不自动 push

## 禁止行为

- 不得自动执行 `git push`，必须由用户手动触发（遵守 CLAUDE.md 规定）
- 不得修改 README.md 以外的文件内容

