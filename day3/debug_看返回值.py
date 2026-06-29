"""
临时脚本：看看 requests.post() 返回的东西到底长什么样
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
data = {
    "model": "deepseek-chat",
    "messages": [
        {"role": "user", "content": "1+1等于几？只回答数字"},
    ],
    "temperature": 0.0,
}

# ===== 发请求 =====
response = requests.post(url, headers=headers, json=data)

# ===== 看看 response 是什么类型 =====
print("1. response 的类型：")
print(f"   {type(response)}")
print()

# ===== 看看 response 有哪些属性 =====
print("2. response 的常用属性：")
print(f"   response.status_code = {response.status_code}")
print(f"   response.ok = {response.ok}")
print()

# ===== 看看原始文字（没解析的） =====
print("3. response.text（原始字符串，前300字符）：")
print(f"   {response.text[:300]}")
print()

# ===== 看看解析后的 Python 字典 =====
print("4. response.json() 解析后的 Python 字典（完整、分行）：")
result = response.json()
print(result)
print(json.dumps(result, ensure_ascii=False, indent=2))
print()

# ===== 看看每一层的类型 =====
print("5. 逐层类型：")
print(f"   response.json()         → {type(result)}")
print(f"   result['choices']       → {type(result['choices'])}  长度={len(result['choices'])}")
print(f"   result['choices'][0]    → {type(result['choices'][0])}")
print(f"   choices[0]['message']   → {type(result['choices'][0]['message'])}")
print(f"   message['content']      → {type(result['choices'][0]['message']['content'])}")
print()

# ===== 最后取到答案 =====
print("6. 取出最终答案：")
answer = result["choices"][0]["message"]["content"]
print(f"   {answer}")
