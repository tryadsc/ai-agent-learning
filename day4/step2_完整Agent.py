"""
Day 4 - 第二步：完整 Agent v1.0（用 Function Calling）

相比 Day 3 的改进：
1. 不用 parse_action() 解析文字了 → 用 API 原生的 tool_calls
2. 加了时间工具
3. 加了错误处理
4. 保留了对话记忆
"""

import requests
import json
from datetime import datetime

with open("./.deepseek_key", "r") as f:
    api_key = f.read().strip()

url = "https://api.deepseek.com/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}


# ===== 工具实现 =====
def calculator(expression):
    """计算器"""
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return f"计算结果：{result}"
    except Exception as e:
        return f"计算出错：{e}"


def get_weather(city):
    """模拟天气查询"""
    weather_db = {
        "广州": "多云，28°C ~ 35°C，湿度 70%，有雷阵雨",
        "北京": "晴，22°C ~ 30°C，湿度 30%",
        "上海": "小雨，25°C ~ 31°C，湿度 80%",
    }
    return weather_db.get(city, f"{city}：晴天，约 25°C")


def get_current_time(_=None):
    """获取当前时间"""
    return datetime.now().strftime("%Y年%m月%d日 %H:%M:%S，星期%w")


# ===== 工具定义（JSON Schema）=====
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "计算数学表达式",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "数学表达式"}
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询城市天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名"}
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "获取当前日期和时间",
            "parameters": {
                "type": "object",
                "properties": {},
            }
        }
    }
]

# 工具名 → 工具函数 的映射
TOOL_MAP = {
    "calculator": calculator,
    "get_weather": get_weather,
    "get_current_time": get_current_time,
}


# ===== Agent 类 =====
class Agent:
    def __init__(self):
        self.api_key = api_key
        self.memory = []  # 对话记忆

    def chat(self, user_input):
        """跟 Agent 对话。自动决定是否调工具，维护记忆。"""

        # 把用户输入加入记忆
        self.memory.append({"role": "user", "content": user_input})

        # System Prompt
        messages = [
            {"role": "system", "content": "你是一个有用的助手。需要时调用工具获取信息，然后回答问题。"}
        ] + self.memory

        # ReAct 循环
        for step in range(5):
            # 调 LLM（带上 tools）
            data = {
                "model": "deepseek-chat",
                "messages": messages,
                "tools": TOOLS,
                "temperature": 0.0,
            }

            try:
                response = requests.post(url, headers=headers, json=data, timeout=30)
                response.raise_for_status()
                result = response.json()
                choice = result["choices"][0]
                message = choice["message"]

                # 情况 1：模型要调工具
                if message.get("tool_calls"):
                    tool_call = message["tool_calls"][0]
                    func_name = tool_call["function"]["name"]
                    func_args = json.loads(tool_call["function"]["arguments"])

                    print(f"   🔧 调用工具：{func_name}({func_args})")

                    # 执行工具
                    func = TOOL_MAP.get(func_name)
                    if func:
                        # 不同工具参数名不同，统一用 **kwargs 传
                        tool_result = func(**func_args)
                    else:
                        tool_result = f"错误：未知工具 {func_name}"

                    print(f"   📋 返回：{tool_result}")

                    # 把工具调用和结果加入对话
                    messages.append({
                        "role": "assistant",
                        "content": None,
                        "tool_calls": [tool_call]
                    })
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "content": tool_result
                    })

                    # 下一轮循环，LLM 会看到工具结果并决定下一步
                    continue

                # 情况 2：模型直接回答
                if message.get("content"):
                    reply = message["content"]
                    self.memory.append({"role": "assistant", "content": reply})
                    return reply

            except requests.exceptions.Timeout:
                print("   ⚠️ 请求超时，重试中...")
                continue
            except requests.exceptions.RequestException as e:
                return f"网络错误：{e}"
            except (KeyError, IndexError, json.JSONDecodeError) as e:
                return f"解析响应出错：{e}"

        return "抱歉，Agent 在规定的步数内没有得出答案。"

    def forget(self):
        """清空记忆"""
        self.memory = []


# ===== 测试 =====
if __name__ == "__main__":
    agent = Agent()

    print("=" * 60)
    print("🧪 测试 1：计算")
    print(f"👤 用户：(100 + 200) * 3 等于多少？")
    print(f"🤖 Agent：{agent.chat('(100 + 200) * 3 等于多少？')}")
    print()

    print("=" * 60)
    print("🧪 测试 2：天气")
    print(f"👤 用户：广州今天天气怎么样？适合出门吗？")
    print(f"🤖 Agent：{agent.chat('广州今天天气怎么样？适合出门吗？')}")
    print()

    print("=" * 60)
    print("🧪 测试 3：时间")
    print(f"👤 用户：现在是几点？")
    print(f"🤖 Agent：{agent.chat('现在是几点？')}")
    print()

    print("=" * 60)
    print("🧪 测试 4：多轮对话——Agent记得之前说过什么吗？")
    print(f"👤 用户：我刚才问过天气吗？是哪个城市的？")
    print(f"🤖 Agent：{agent.chat('我刚才问过天气吗？是哪个城市的？')}")
    print()

    print(f"📝 memory 里有 {len(agent.memory)} 条消息")
