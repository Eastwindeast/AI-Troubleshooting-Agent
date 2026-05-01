# 🚀 AI-Driven Autonomous Troubleshooting Agent

This is an autonomous **SRE Troubleshooting Agent** prototype built with LLMs. It mimics the standard incident response path: **Alert -> Log Retrieval -> Stacktrace Analysis -> Code Change Correlation -> Root Cause Analysis**.

## 🌟 Key Features
- **Autonomous Reasoning**: Dynamically decides whether to fetch logs or git commits based on context.
- **Cross-Domain Correlation**: Links infrastructure logs with application code changes to find the "smoking gun".
- **Production Ready**: Uses `.env` for secure key management and modular function calling.

## 🛠️ Tech Stack
- **LLM**: GPT-4o / DeepSeek (Models supporting Tool Calling)
- **Framework**: OpenAI SDK / Python
- **Env Management**: python-dotenv

## 🚀 Quick Start
1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Configure Environment**:
   - Rename `.env.example` to `.env`.
   - Fill in your `OPENAI_API_KEY`.
3. **Run Demo**:
   ```bash
   python main.py
   ```
