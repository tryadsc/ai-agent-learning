"""
Day 2 - 第一步：最简单的 LLM 调用（10行代码）

运行前准备：
    在项目根目录创建一个文件叫 .deepseek_key
    里面只放你的 API Key（sk- 开头的那串），别的什么都不要放
"""

import requests
import json

# 1. 读取 API Key
with open(".deepseek_key", "r") as f:
    api_key = f.read().strip()

# 2. 准备要发送的数据
url = "https://api.deepseek.com/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}
data = {
    "model": "deepseek-chat",
    "messages": [
        {"role": "system", "content": "你是一个有用的助手"},
        {"role": "user", "content": "用Python写一个快速排序"},
    ],
    "temperature": 0.7,
}

# 3. 发送请求、获取结果
response = requests.post(url, headers=headers, json=data)
result = response.json()

# 4. 只打印模型回复的内容
print(result["choices"][0]["message"]["content"])
