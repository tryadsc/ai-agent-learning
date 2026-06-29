# Day 1 回顾：Python 核心语法（Agent 开发必备）

> 日期：2026-06-28

---

## 1. 列表推导式

一行代码生成新列表。

```python
[对元素做什么  for  元素  in  原列表  if  条件]

# 举例
[n**2 for n in [1,2,3,4,5] if n%2==0]   # → [4, 16]
[str(n) for n in nums if n>3]            # → ['4', '5', '6']

# 字典版
{index: value for index, value in enumerate(keys)}
```

---

## 2. `*args` 和 `**kwargs`

处理不确定数量的参数。

```python
# *args → 把多余的位置参数打包成元组
def f(*args):
    print(args)      # (1, 2, 3)

# **kwargs → 把 key=value 的参数打包成字典
def f(**kwargs):
    print(kwargs)    # {'model': 'gpt-4', 'temp': 0.7}

# 组合
def f(name, *tools, **config):
    pass
```

---

## 3. lambda — 一句话函数

```python
lambda 输入: 输出

square = lambda x: x**2
add = lambda a, b: a + b

# 真实场景：排序
tools.sort(key=lambda t: t["priority"])
```

---

## 4. 装饰器 `@` — 给函数套壳

```python
@tool
def func():
    pass

# 等于 ↓
func = tool(func)
```

---

## 5. 类 class — 把数据+行为打包

```python
class Tool:
    def __init__(self, name, description, func):  # 出厂设置
        self.name = name
        self.description = description
        self.func = func

    def run(self, input_text):  # 方法
        return self.func(input_text)

# 使用
weather = Tool("天气", "查天气", get_weather)
weather.run("广州")
```

### 关键点
- `__init__` = 出厂设置，创建实例时自动跑
- `self` = 我自己，引用当前实例
- **方法定义后面必须有冒号 `:`**
- **字典的 key:value 用冒号，不是逗号**

---

## 6. 练手成果：Memory 类

```python
class Memory:
    def __init__(self):
        self.messages = []

    def add_message(self, role, content):
        ms = {"role": role, "content": content}
        self.messages.append(ms)

    def get_history(self):
        return self.messages

    def clear(self):
        self.messages.clear()
```

---

## ⚠️ 常见失误

| 错误 | 正确 |
|------|------|
| `{"key", value}` | `{"key": value}` |
| `def func(self)` | `def func(self):` |
| `self.message = []` | `self.messages = []` |
