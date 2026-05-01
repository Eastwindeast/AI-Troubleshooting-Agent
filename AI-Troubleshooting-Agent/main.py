import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Client Initialization
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
)

MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o")

# --- Mock Enterprise System Tools ---

def fetch_system_logs(service_name: str) -> str:
    print(f"🔧 [Tool Call]: Fetching latest logs for {service_name}...")
    return """
    [ERROR] 2026-05-01 10:20:05 - NullPointerException in BillingService.java:214
    Stacktrace: 
      at com.app.billing.Engine.calculate(BillingService.java:214)
    Message: 'user_tier' object is null.
    """

def fetch_git_commits(service_name: str) -> str:
    print(f"🔧 [Tool Call]: Fetching recent commits for {service_name}...")
    return """
    Commit: d9f2e1a
    Author: Mike Chen
    Date: 2 hours ago
    Message: "Refactored user profile loading logic."
    Modified: BillingService.java
    """

# --- Agent Core Logic ---

def run_agent(alert_msg):
    print(f"🚨 [Alert Received]: {alert_msg}\n")
    
    tools = [
        {
            "type": "function",
            "function": {
                "name": "fetch_system_logs",
                "description": "Fetch error logs and stacktrace for a specific service",
                "parameters": {
                    "type": "object",
                    "properties": {"service_name": {"type": "string"}},
                    "required": ["service_name"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "fetch_git_commits",
                "description": "Retrieve recent git commit history for a specific service",
                "parameters": {
                    "type": "object",
                    "properties": {"service_name": {"type": "string"}},
                    "required": ["service_name"]
                }
            }
        }
    ]

    messages = [
        {"role": "system", "content": "You are a senior SRE Expert. Use tools to analyze the root cause and provide a report."},
        {"role": "user", "content": alert_msg}
    ]

    response = client.chat.completions.create(model=MODEL_NAME, messages=messages, tools=tools)
    response_message = response.choices[0].message
    messages.append(response_message)

    if response_message.tool_calls:
        for tool_call in response_message.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            if name == "fetch_system_logs":
                res = fetch_system_logs(args['service_name'])
            else:
                res = fetch_git_commits(args['service_name'])
            
            messages.append({"tool_call_id": tool_call.id, "role": "tool", "name": name, "content": res})

        final_res = client.chat.completions.create(model=MODEL_NAME, messages=messages)
        print("\n📝 [Final Root Cause Analysis]:")
        print("-" * 50)
        print(final_res.choices[0].message.content)
        print("-" * 50)

if __name__ == "__main__":
    run_agent("P0 Alert: billing-service experiencing 100% error rate in prod.")
