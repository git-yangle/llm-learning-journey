# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Personal 15-day learning journey for LLM application development and AI Coding. The repository evolves daily, progressing through Python fundamentals, MCP protocol, and ultimately building a full-stack LLM chat application.

## Learning Structure

- **Days 1–3**: Python modern features (Type Hints, asyncio, pydantic) + LLM API basics
- **Days 4–7**: Claude Code workflow + MCP (Model Context Protocol) custom server development
- **Days 8–14**: Full-stack LLM chat app (RAG, memory, SSE streaming, Streamlit/Gradio frontend)
- **Day 15**: Retrospective

Each day produces practice files named `dayN_*.py` (or similar).

## Environment

- Python managed via **Miniconda**; activate the appropriate conda environment before running scripts.
- Dependencies installed per-day as needed; no single `requirements.txt` yet.
- API keys stored in `.env` (gitignored); load with `python-dotenv` or similar.

## Running Practice Scripts

```bash
# Run a day's practice script
python dayN_practice.py

# Example: Day 2 asyncio demo
python day2_practice.py
```

## Key Technologies by Phase

| Phase | Stack |
|-------|-------|
| Python basics | `pydantic`, `asyncio`, `typing` |
| LLM API | Anthropic SDK / OpenAI SDK, token/temperature concepts |
| MCP | Python MCP SDK, custom MCP Server |
| Chat app backend | Go or Python, SSE streaming |
| Chat app frontend | Streamlit or Gradio |
| RAG | LangChain or LlamaIndex |
