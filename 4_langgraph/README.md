---
title: sidekick
emoji: 🤖
colorFrom: green
colorTo: green
sdk: gradio
sdk_version: 5.49.1
app_file: app.py
pinned: false
---

# Sidekick Personal Co-Worker

An AI-powered assistant that helps you complete tasks using multiple tools including web browsing, file management, Python code execution, and more.

## Features

- **Multi-agent workflow**: Uses a worker-evaluator pattern to ensure tasks are completed correctly
- **Web browsing**: Can navigate and retrieve information from web pages
- **File management**: Can create, read, and manage files
- **Python execution**: Can run Python code to perform calculations or data processing
- **Web search**: Integrates with Google Search API
- **Wikipedia access**: Can look up information from Wikipedia

## Setup

1. Set your OpenAI API key as an environment variable: `OPENAI_API_KEY`
2. Optionally set `PUSHOVER_TOKEN` and `PUSHOVER_USER` for push notifications
3. Optionally set `SERPER_API_KEY` for web search functionality

## Usage

1. Enter your request in the message box
2. Specify your success criteria
3. Click "Go!" or press Enter
4. The assistant will work on your task and provide feedback

## Files Required

- `app.py` - Main Gradio application
- `sidekick.py` - Sidekick class with LangGraph workflow
- `sidekick_tools.py` - Tools for web browsing, file management, etc.

