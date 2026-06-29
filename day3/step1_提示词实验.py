"""
Day 3 - 第一步：Prompt Engineering 实验

同一个问题，换 System Prompt 就换一种回答方式。
"""

import requests

# 读取 API Key
with open("./.deepseek_key", "r") as f:
    api_key = f.read().strip()

url = "https://api.deepseek.com/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}

question = "帮我写一段代码，计算斐波那契数列前20项。"


def ask(system_prompt, temperature=0.3):
    """发请求，返回模型回答"""
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
        "temperature": temperature,
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]


# ===== 实验 1：普通回答 =====
print("=" * 60)
print("📋 实验 1：普通 prompt")
print("=" * 60)
print(ask("你是一个编程助手。")[:400])
print()

# ===== 实验 2：Chain-of-Thought =====
print("=" * 60)
print("📋 实验 2：加「让我们一步一步思考」")
print("=" * 60)
print(ask(
    "你是一个编程助手。回答问题前，先写「思考：...」分析问题，再写「代码：...」给出答案。"
)[:500])
print()

# ===== 实验 3：Few-shot（给例子）=====
print("=" * 60)
print("📋 实验 3：Few-shot —— 给例子让它模仿格式")
print("=" * 60)
print(ask(
    """你是一个编程老师。回答必须遵循这个格式：

【问题分析】1-2句话
【代码】Python完整代码
【复杂度】时间+空间

示例（用户问冒泡排序时）：
【问题分析】冒泡排序通过相邻元素两两比较交换，将最大元素冒到末尾。
【代码】
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
【复杂度】时间O(n²)，空间O(1)

现在回答用户的问题。"""
)[:600])
print()

# ===== 实验 4：强制输出 JSON =====
print("=" * 60)
print("📋 实验 4：强制输出 JSON（Agent开发必备）")
print("=" * 60)
print(ask(
    '你是一个数据接口。只输出纯JSON，不要任何多余文字。'
    '格式：{"language":"...", "function_name":"...", "code":"...", "explanation":"..."}',
    temperature=0.2
)[:500])
print()

print("=" * 60)
print("💡 四个实验对应四种 Prompt 技巧：")
print("   1 → 基础 prompt（随便答）")
print("   2 → Chain-of-Thought（逐步推理，质量更高）")
print("   3 → Few-shot（给例子，控制格式）")
print("   4 → Structured Output（输出 JSON，方便代码解析）")
