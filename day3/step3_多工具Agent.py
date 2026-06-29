"""
Day 3 - 第三步：多工具 Agent

比 step2 多了一个工具——搜索引擎。
Agent 需要自己决定：该用计算器？还是搜东西？还是直接回答？
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


# ===== 工具 1：计算器 =====
def calculator(expression):
    """安全计算"""
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return f"计算结果：{result}"
    except Exception as e:
        return f"计算出错：{e}"


# ===== 工具 2：模拟搜索（不调真实 API，用字典模拟） =====
SEARCH_DB = {
    "广州天气": "广州今天多云，28°C ~ 35°C，湿度 70%",
    "python": "Python 是一种解释型、面向对象的高级编程语言，由 Guido van Rossum 于 1991 年创建。",
    "小鹏汽车": "小鹏汽车成立于 2014 年，总部位于广州，是中国领先的智能电动汽车公司。",
    "2026世界杯": "2026 年世界杯由美国、加拿大、墨西哥联合举办，共 48 支球队参赛。",
}


def search(keyword):
    """模拟搜索，从本地字典查"""
    for key, value in SEARCH_DB.items():
        if keyword.lower() in key.lower():
            return value
    # 如果本地没找到，用关键词本身模拟返回
    return f"关于「{keyword}」的搜索结果：这是一个模拟结果。（后续可以接入真实搜索 API）"


# ===== LLM 调用 =====
def call_llm(messages):
    data = {
        "model": "deepseek-chat",
        "messages": messages,
        "temperature": 0.0,
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]


# ===== 解析器（支持两种工具）=====
def parse_action(llm_output):
    """解析 LLM 输出，判断是用计算器 / 搜索 / 回答"""
    lines = llm_output.strip().split("\n")
    result = {"type": "", "tool_name": "", "tool_input": "", "answer": ""}

    for line in lines:
        line = line.strip()

        if line.startswith("行动："):
            action_text = line.split("：", 1)[-1].strip()

            if action_text.startswith("CALCULATE("):
                result["type"] = "action"
                result["tool_name"] = "calculator"
                result["tool_input"] = action_text[len("CALCULATE("):-1]

            elif action_text.startswith("SEARCH("):
                result["type"] = "action"
                result["tool_name"] = "search"
                result["tool_input"] = action_text[len("SEARCH("):-1]

        elif line.startswith("回答："):
            result["type"] = "answer"
            result["answer"] = line.split("：", 1)[-1].strip()

    return result


# ===== 工具执行器 =====
def execute_tool(tool_name, tool_input):
    """根据工具名调用对应的工具"""
    if tool_name == "calculator":
        return calculator(tool_input)
    elif tool_name == "search":
        return search(tool_input)
    else:
        return f"错误：未知工具 {tool_name}"


# ===== Agent 主循环 =====
def agent(question, max_steps=5):
    messages = [
        {"role": "system", "content": """你是一个能用工具的 Agent。你有以下工具：

1. CALCULATE(表达式) - 计算数学表达式，例如 CALCULATE(100*200)
2. SEARCH(关键词) - 搜索信息，例如 SEARCH(广州天气)

严格遵循以下格式：

需要计算时：
思考：我需要计算
行动：CALCULATE(表达式)

需要搜索信息时：
思考：我需要搜索
行动：SEARCH(关键词)

可以回答时：
思考：信息足够了
回答：最终答案

注意：
- 每次只能写一个「行动」
- 拿到工具结果后，判断是否需要继续用工具，还是已经可以回答"""},
        {"role": "user", "content": question},
    ]

    print("=" * 60)
    print(f"👤 用户：{question}\n")

    for step in range(1, max_steps + 1):
        print(f"--- 第 {step} 步 ---")
        llm_output = call_llm(messages)
        print(f"🤖 LLM：\n{llm_output}\n")
        parsed = parse_action(llm_output)

        if parsed["type"] == "answer":
            print(f"✅ 答案：{parsed['answer']}")
            return parsed["answer"]

        elif parsed["type"] == "action":
            tool_result = execute_tool(parsed["tool_name"], parsed["tool_input"])
            print(f"🔧 {parsed['tool_name']}({parsed['tool_input']})")
            print(f"📋 结果：{tool_result}\n")

            messages.append({"role": "assistant", "content": llm_output})
            messages.append({"role": "user", "content": f"工具返回：{tool_result}"})

        else:
            print("⚠️ 格式不对，提醒重试\n")
            messages.append({"role": "assistant", "content": llm_output})
            messages.append({"role": "user", "content": "请严格按格式输出：思考→行动或回答"})

    return "超过步数限制"


# ===== 测试 =====
if __name__ == "__main__":
    print("🧪 测试 1：需要计算")
    agent("(100 + 200) * 3 等于多少？")

    print()
    print("🧪 测试 2：需要搜索")
    agent("广州今天天气怎么样？")

    print()
    print("🧪 测试 3：需要搜索 + 不需要工具")
    agent("小鹏汽车是哪里的公司？")

    print()
    print("🧪 测试 4：不需要工具")
    agent("解释一下什么是 Python")
