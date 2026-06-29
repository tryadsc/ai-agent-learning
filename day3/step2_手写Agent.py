"""
Day 3 - 第二步：手写 ReAct Agent（最简版）

Agent = LLM + 工具 + 循环

这个 Agent 只有一个工具——计算器。
但它演示了 Agent 的核心循环：思考 → 行动 → 观察 → 再思考 → 最终回答
"""

import requests
import json

# 读取 API Key
with open("./.deepseek_key", "r") as f:
    api_key = f.read().strip()

url = "https://api.deepseek.com/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}


# ===== 工具：计算器 =====
def calculator(expression):
    """安全计算数学表达式，返回结果"""
    try:
        # eval 有风险，但这里只是学习用
        result = eval(expression, {"__builtins__": {}}, {})
        return f"计算结果：{result}"
    except Exception as e:
        return f"计算出错：{e}"


# ===== LLM 调用函数 =====
def call_llm(messages):
    """把 messages 发给 DeepSeek，返回模型说的一句话"""
    data = {
        "model": "deepseek-chat",
        "messages": messages,
        "temperature": 0.0,  # Agent 场景用低温，保证稳定
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]


# ===== 解析模型的输出 =====
def parse_action(llm_output):
    """
    模型输出格式：
        思考：xxx
        行动：CALCULATE(1+2+3)
    或者：
        思考：xxx
        回答：yyy

    返回一个字典：{"type": "action" 或 "answer", ...}
    """
    lines = llm_output.strip().split("\n")
    result = {"thought": "", "type": "", "action": "", "answer": ""}

    for line in lines:
        line = line.strip()
        if line.startswith("思考：") or line.startswith("Thought:"):
            result["thought"] = line.split("：", 1)[-1].split(":", 1)[-1].strip()
        elif line.startswith("行动：") or line.startswith("Action:"):
            action_text = line.split("：", 1)[-1].split(":", 1)[-1].strip()
            result["type"] = "action"
            # 解析 CALCULATE(表达式)
            if action_text.upper().startswith("CALCULATE("):
                result["action"] = action_text[len("CALCULATE("):-1]  # 去掉括号
        elif line.startswith("回答：") or line.startswith("Answer:"):
            result["type"] = "answer"
            result["answer"] = line.split("：", 1)[-1].split(":", 1)[-1].strip()

    return result


# ===== 核心：ReAct 循环 =====
def agent(question, max_steps=5):
    """
    Agent 的主循环。

    参数:
        question: 用户的问题
        max_steps: 最多思考-行动几轮，防止死循环

    返回:
        最终答案
    """
    # 初始化对话——System Prompt 是关键！
    messages = [
        {"role": "system", "content": """你是一个能用工具的 Agent。严格遵循以下格式回复：

当你需要计算时：
思考：我需要计算xxx
行动：CALCULATE(数学表达式)

当你可以回答时：
思考：我已经得到足够的信息
回答：最终答案

注意：
- 每次只能写一个「行动」，不要写多个
- 行动只能是 CALCULATE()，括号里放纯数学表达式
- 只有拿到计算结果后才能写「回答」
- 不要在「行动」后面跟任何其他内容"""},
        {"role": "user", "content": question},
    ]

    print("=" * 60)
    print(f"👤 用户问：{question}\n")

    for step in range(1, max_steps + 1):
        print(f"--- 第 {step} 步 ---")

        # 1. 调用 LLM
        llm_output = call_llm(messages)
        print(f"🤖 LLM 输出：\n{llm_output}\n")

        # 2. 解析输出
        parsed = parse_action(llm_output)

        # 3. 如果模型要回答 → 结束
        if parsed["type"] == "answer":
            print(f"✅ 最终答案：{parsed['answer']}")
            return parsed["answer"]

        # 4. 如果模型要行动 → 执行工具，返回观察结果
        if parsed["type"] == "action":
            if parsed["action"]:
                tool_result = calculator(parsed["action"])
                print(f"🔧 工具结果：{tool_result}\n")
            else:
                tool_result = "错误：没有指定要计算什么"

            # 把模型的输出和工具结果都记到对话里
            messages.append({"role": "assistant", "content": llm_output})
            messages.append({"role": "user", "content": f"观察结果：{tool_result}"})

        else:
            # 模型没有按格式输出 → 提示它
            print("⚠️ 模型输出格式不对，提醒它重试\n")
            messages.append({"role": "assistant", "content": llm_output})
            messages.append({"role": "user", "content": "请按照格式输出：先写「思考：...」，再写「行动：CALCULATE(...)」或「回答：...」"})

    # 超过最大步数
    return "抱歉，Agent 在规定的步数内没有得出答案。"


# ===== 测试 =====
if __name__ == "__main__":
    print("🧪 测试 1：简单计算")
    agent("(3 + 5) * 2 等于多少？")

    print()
    print("🧪 测试 2：需要两步计算")
    agent("计算 12345 + 67890 的结果，然后把结果的每位数字加起来。")

    print()
    print("🧪 测试 3：普通问题（不需要工具）")
    agent("Python 是什么？")
