"""
Day 4 - 第一步：真正的 Function Calling

跟 Day 3 的区别：
    不靠"读文字猜模型想用什么工具"了
    而是告诉 API 工具的定义（JSON Schema），模型直接返回结构化的调用信息
"""

import requests
import json

with open("./.deepseek_key", "r") as f:
    api_key = f.read().strip()

url = "https://api.deepseek.com/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}


# ===== 定义工具（JSON Schema 格式）=====
# 这就是告诉模型："我有这些工具，每个工具的参数长这样"
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "计算数学表达式，支持加减乘除和括号",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "要计算的数学表达式，例如 '1+2*3'"
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询指定城市的天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名，例如 '广州'、'北京'"
                    }
                },
                "required": ["city"]
            }
        }
    }
]


# ===== 工具实现 =====
def calculator(expression):
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return f"计算结果：{result}"
    except Exception as e:
        return f"计算出错：{e}"


def get_weather(city):
    # 模拟天气数据
    weather_db = {
        "广州": "多云，28°C ~ 35°C，湿度 70%",
        "北京": "晴，22°C ~ 30°C，湿度 30%",
        "上海": "小雨，25°C ~ 31°C，湿度 80%",
    }
    return weather_db.get(city, f"{city}：晴天，20°C")


# ===== 测试：看看 Function Calling 的返回长什么样 =====
messages = [
    {"role": "system", "content": "你是一个助手。需要时调用工具。"},
    {"role": "user", "content": "广州今天天气怎么样？"},
]

data = {
    "model": "deepseek-chat",
    "messages": messages,
    "tools": tools,          # ← 关键！传工具定义进去
    "temperature": 0.0,
}

response = requests.post(url, headers=headers, json=data)
result = response.json()

print("=" * 60)
print("📦 完整响应（有 function calling 时）：")
print(json.dumps(result, ensure_ascii=False, indent=2)[:1500])
print()

# ===== 看看 choice 里的 message 跟普通聊天有什么不同 =====
choice = result["choices"][0]
message = choice["message"]

print("=" * 60)
print("🔍 message 内容：")
print(f"   content = {message.get('content')}")
print(f"   tool_calls = {json.dumps(message.get('tool_calls'), ensure_ascii=False, indent=4)}")
print()

# ===== 如果有 tool_calls，提取出来 =====
if message.get("tool_calls"):
    tool_call = message["tool_calls"][0]
    func_name = tool_call["function"]["name"]
    func_args = json.loads(tool_call["function"]["arguments"])

    print("=" * 60)
    print(f"🔧 模型要调用的工具：{func_name}")
    print(f"📝 参数：{func_args}")
    print()

    # 执行工具
    if func_name == "calculator":
        result = calculator(func_args["expression"])
    elif func_name == "get_weather":
        result = get_weather(func_args["city"])
    else:
        result = "未知工具"

    print(f"📋 工具返回：{result}")
    print()
    print("💡 这就是 Function Calling —— 模型返回的不是文字，是结构化的工具调用！")
    print("   不用 parse_action() 去猜了，直接取 JSON 就行。")
