"""
Day 2 - 第二步：让模型"记得"之前说过什么

核心思路（就一句话）：
    把之前的对话全部塞回给模型 → 它就能"记住"

类比：
    模型 = 金鱼，每次醒来都失忆
    history = 你拿小本本把每句话记下来，下次给金鱼看
"""

import requests
import json

# 1. 读取 API Key
with open(".deepseek_key", "r") as f:
    api_key = f.read().strip()

url = "https://api.deepseek.com/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}

# 2. 这个函数就是 step1 的逻辑，抽出来方便复用
def chat(user_input, history=None):
    """
    调用 DeepSeek 聊天。

    参数:
        user_input: 你这次说的话
        history:    之前的所有对话记录（列表）

    返回:
        模型的回复文字
    """
    # 构建消息列表
    messages = [
        {"role": "system", "content": "你是一个编程助教，用中文回答。"}
    ]

    # ★ 关键！如果有历史记录，拼进去
    if history:
        messages = messages + history  # 把历史的对话接在后面

    # 最后加上用户这次的问题
    messages.append({"role": "user", "content": user_input})

    # 发送请求
    data = {
        "model": "deepseek-chat",
        "messages": messages,
        "temperature": 0.7,
    }
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    return result["choices"][0]["message"]["content"]


# 3. 开始对话
history = []  # ← 这就是我们的小本本

# 第一轮
print("=" * 50)
question1 = "我叫小明，我正在学 Python。"
reply1 = chat(question1, history)
print(f"👤 我: {question1}")
print(f"🤖 AI: {reply1[:200]}")

# ★ 把这一轮的对话记到小本本上
history.append({"role": "user", "content": question1})
history.append({"role": "assistant", "content": reply1})

# 第二轮
print()
question2 = "你还记得我叫什么名字吗？我在学什么？"
reply2 = chat(question2, history)
print(f"👤 我: {question2}")
print(f"🤖 AI: {reply2[:200]}")

history.append({"role": "user", "content": question2})
history.append({"role": "assistant", "content": reply2})

# 第三轮
print()
question3 = "针对我学的语言，给我布置一个练习题。"
reply3 = chat(question3, history)
print(f"👤 我: {question3}")
print(f"🤖 AI: {reply3[:200]}")

print()
print("=" * 50)
print("💡 关键点：")
print(f"   第一轮 history 里只有 {0} 条记录 → 模型不知道你是谁")
print(f"   第二轮 history 里已有 {2} 条记录 → 模型能'回忆'起第一轮内容")
print(f"   第三轮 history 里已有 {4} 条记录 → 模型记得整个对话过程")
print()
print("   history 就是这个作用 —— 把之前的话全部塞回去！")
