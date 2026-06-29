"""
Day 2 - 第三步：把代码打包成一个类

为什么用类？
    之前：每次调 chat(user_input, history)，还要自己维护 history
    现在：bot = ChatBot() → bot.chat("问题") → 自动帮你记

这个类就做三件事：
    1. 保存 api_key（不用每次都读文件）
    2. 保存 history（自动维护，你不用管）
    3. 提供 chat() 方法（直接用）
"""

import requests
import json


class ChatBot:
    """
    一个能记住对话的机器人。

    用法：
        bot = ChatBot()
        bot.chat("我叫小明")        # 第一轮
        bot.chat("我叫什么名字？")   # 第二轮，它记得！
    """

    def __init__(self):
        """创建机器人时做的事：加载密码 + 清空记忆"""
        with open(".deepseek_key", "r") as f:
            self.api_key = f.read().strip()

        self.url = "https://api.deepseek.com/v1/chat/completions"
        self.history = []  # ← 记忆就存在这里

    def chat(self, user_input, temperature=0.7):
        """
        跟机器人聊天。自动维护记忆。
        返回模型的回答。
        """
        # 构建消息：system prompt + 历史 + 当前问题
        messages = [
            {"role": "system", "content": "你是一个有用的助手，用中文回答。"}
        ]
        messages = messages + self.history  # 把之前的对话拼进去
        messages.append({"role": "user", "content": user_input})

        # 发送请求
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        data = {
            "model": "deepseek-chat",
            "messages": messages,
            "temperature": temperature,
        }
        response = requests.post(self.url, headers=headers, json=data)
        result = response.json()
        reply = result["choices"][0]["message"]["content"]

        # ★ 自动记录——你不需要手动 append 了
        self.history.append({"role": "user", "content": user_input})
        self.history.append({"role": "assistant", "content": reply})

        return reply

    def forget(self):
        """清空记忆，重新开始对话"""
        self.history = []


# ===== 测试 =====
if __name__ == "__main__":
    bot = ChatBot()

    print("🤖 第一轮：")
    print(bot.chat("我叫小明，我在学 Python。", temperature=0.7))
    print()

    print("🤖 第二轮（应该记得名字）：")
    print(bot.chat("我叫什么名字？我刚才说我在学什么？", temperature=0.7))
    print()

    print("🤖 第三轮（应该记得上下文）：")
    print(bot.chat("能给我出一道简单的 Python 题吗？", temperature=0.7))
    print()

    print(f"📝 history 里现在有 {len(bot.history)} 条消息")
