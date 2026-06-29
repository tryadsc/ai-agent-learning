# Day 3 回顾：Prompt 工程 + ReAct Agent

> 日期：2026-06-29

---

## 1. Prompt Engineering 四种技巧

| 技巧 | 一句话 | 示例 |
|------|--------|------|
| System Prompt | 定义模型的"人设"和行为规则 | "你是一个大学教授..." |
| Chain-of-Thought | 让模型先思考再回答 | "先写「思考：...」再写「代码：...」" |
| Few-shot | 给例子，让模型模仿格式 | "示例——如果用户问冒泡排序：..." |
| Structured Output | 强制输出 JSON，方便代码解析 | "只输出纯 JSON，不要任何多余文字" |

---

## 2. Agent 是什么

```
Agent = LLM（大脑） + 工具（手） + 记忆（小本本） + 循环（不断思考-行动）
```

跟普通 ChatBot 的区别：ChatBot 只会聊天，Agent 能调工具干活。

---

## 3. ReAct 循环

```
思考 → 行动 → 观察 → 思考 → ... → 最终回答
```

每次循环：
1. 调 LLM → 模型输出"思考：... 行动：XXX(...)"
2. parse_action() 解析 → 判断是要行动还是要回答
3. 如果要行动 → 执行工具 → 结果喂回 LLM → 下一轮
4. 如果要回答 → 返回答案，结束

---

## 4. parse_action() — 连接 LLM 和工具的关键

```python
# LLM 输出（字符串）
"思考：需要计算\n行动：CALCULATE(1+2)"

# parse_action() 解析成字典
{"type": "action", "tool_name": "calculator", "tool_input": "1+2"}

# Agent 根据 type 决定：继续循环还是返回答案
```

---

## 5. 多工具 Agent

工具再多，逻辑一样——只需两处改动：
- System Prompt 列出所有工具
- execute_tool() 根据 tool_name 分发到对应函数

模型自己从 System Prompt 里看有哪些工具，自己决定调哪个。

---

## ⚠️ 踩坑

| 问题 | 解决 |
|------|------|
| `response.text` 是字符串，不能 `[]` 取值 | 用 `response.json()` 解析成字典 |
| Agent 比 ChatBot 调更多次 LLM | Agent 每次行动后要再来一轮，直到模型说"回答" |

---

## 代码产出

- `day3/step1_提示词实验.py` — 4种 prompt 技巧对比
- `day3/step2_手写Agent.py` — 单工具 ReAct Agent（计算器）
- `day3/step3_多工具Agent.py` — 多工具 Agent（计算器 + 搜索）
- `day3/debug_看返回值.py` — 查看 API 响应结构
