# 🎯 10天 AI Agent 实习冲刺计划

> **目标画像**：研一AI专业，Python入门基础，坐标广州，每天5-7小时，10天后投递Agent实习岗
> **开始日期**：2026年6月28日 | **投递日期**：2026年7月8日起

---

## 📊 广州 Agent 实习市场速览

| 公司 | 岗位方向 | 薪资参考 | 门槛 |
|------|----------|----------|------|
| 小鹏汽车 | AI Agent开发（通用智能平台） | 6K-7.5K/月 | ⭐⭐⭐ |
| 文基智能 | 算法开发（RAG与Agent方向） | 200-250元/天 | ⭐⭐ |
| 智算引擎技术 | AI技术转化研究员 | 4K-8K/月 | ⭐⭐ |
| 彩讯科技(RichAI) | 高潜AI工程师（大模型/Agent） | 200-500元/天 | ⭐⭐⭐⭐⭐ |
| 中国移动 | AI产品开发实习生 | 面议 | ⭐⭐ |
| 阿科玛(Arkema) | AI实习生（工厂AI Agent） | 面议 | ⭐⭐⭐ |

**你的核心竞争策略**：主攻中小公司（文基智能、智算引擎），同时冲刺小鹏。核心卖点是「有完整Agent项目 + 硕士学历」。

---

## 🗺️ 10天学习路线总览

```
Day 1-2  │ Day 3-4  │ Day 5-6  │ Day 7-8  │ Day 9-10
筑基期   │ 核心技能  │ 框架实战  │ 项目冲刺  │ 面试冲刺
Python   │ Agent原理 │ LangChain│ 完整项目  │ 八股+简历
+ LLM    │ +ToolCall│ +RAG     │ +GitHub  │ +投递
```

---

## 📅 Day 1-2：Python强化 + LLM初体验

### Day 1（6小时）：Python核心能力补强

> 广州岗位JD里「扎实的Python编程能力」是出现频率最高的要求

**上午（3h）：Python进阶语法**
- [ ] 列表推导式、字典推导式 → 写5个练习
- [ ] 函数进阶：`*args` `**kwargs`、lambda、装饰器（理解即可）
- [ ] 类（class）：`__init__`、继承、`@property` → 写一个简单的类
- [ ] 异常处理：`try/except/finally`
- [ ] 文件读写：`with open()` + `json` 模块

**下午（3h）：Python工程基础**
- [ ] `requests` 库：发GET/POST请求，处理JSON响应
- [ ] `asyncio` 基础概念（了解async/await即可，Agent开发中大量使用）
- [ ] 虚拟环境：`python -m venv` 创建和使用
- [ ] Git基础：`git init` `git add` `git commit` `git push`
- [ ] **练手**：用requests爬一个公开API（如天气API），解析JSON并打印

**资源**：
- Python官方教程（中文）: https://docs.python.org/zh-cn/3/tutorial/
- 菜鸟教程Python快速复习: https://www.runoob.com/python3/

---

### Day 2（6小时）：LLM基础 + 第一个API调用

**上午（3h）：理解LLM**
- [ ] Transformer基本原理（理解Attention是什么即可，不需要手写）
  - 看李沐《动手学深度学习》Transformer章节（1.5h）
  - 核心理解：输入→编码→注意力→解码→输出的流程
- [ ] 主流模型认知：GPT-4o、Claude、DeepSeek、Qwen、GLM各有什么特点
- [ ] Token是什么？Context Window是什么？Temperature/Top-P怎么调？

**下午（3h）：动手！调用第一个大模型API**
- [ ] 注册DeepSeek平台账号（https://platform.deepseek.com/），获取API Key
  - 超便宜，新用户送500万token，足够学习
- [ ] 用Python调用DeepSeek API完成一个对话
```python
import requests
import json

url = "https://api.deepseek.com/v1/chat/completions"
headers = {"Authorization": "Bearer YOUR_API_KEY", "Content-Type": "application/json"}
data = {
    "model": "deepseek-chat",
    "messages": [
        {"role": "system", "content": "你是一个有用的助手"},
        {"role": "user", "content": "用Python写一个快速排序"}
    ],
    "temperature": 0.7
}
response = requests.post(url, headers=headers, json=data)
print(response.json()["choices"][0]["message"]["content"])
```
- [ ] 尝试修改system prompt，观察输出变化
- [ ] 尝试调整temperature参数，观察创造性变化
- [ ] **产出**：一个能调用LLM的Python脚本，放到GitHub仓库

---

## 📅 Day 3-4：Agent核心原理 + 从零手写Agent

### Day 3（6小时）：Prompt Engineering + ReAct范式

**上午（3h）：Prompt Engineering精讲**
- [ ] System Prompt vs User Prompt 的区别和作用
- [ ] Few-shot prompting：给例子让模型模仿
- [ ] Chain-of-Thought（思维链）：让模型"一步步思考"
- [ ] Structured Output：让模型输出JSON格式
- [ ] **练习**：写3个不同场景的prompt（简历分析助手、代码reviewer、周报生成器）

**下午（3h）：理解Agent的核心——ReAct范式**
- [ ] 什么是Agent？Agent = LLM + 工具 + 记忆 + 规划
- [ ] ReAct循环：Thought → Action → Observation → Thought → ... → Final Answer
- [ ] 手写一个简单的ReAct Agent（不用框架！）
  - Agent收到问题 → 思考需要什么工具 → 调用工具 → 观察结果 → 继续思考 → 给出答案
- [ ] **核心练习**：实现一个带计算器和搜索功能的Agent

```python
# ReAct Agent的伪代码框架
def react_agent(question):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.append({"role": "user", "content": question})
    
    for _ in range(MAX_STEPS):  # 最多N步
        response = call_llm(messages)
        action = parse_action(response)  # 解析出Thought和Action
        
        if action.type == "FINAL_ANSWER":
            return action.answer
        
        result = execute_tool(action.tool_name, action.tool_input)
        messages.append({"role": "assistant", "content": response})
        messages.append({"role": "user", "content": f"Observation: {result}"})
```

---

### Day 4（6小时）：Tool Calling + Function Calling

**上午（3h）：深入工具调用**
- [ ] 理解Function Calling机制：模型如何知道该调用哪个函数？
- [ ] JSON Schema：如何定义工具的参数规范
- [ ] 实现3个工具：
  1. 天气查询工具（调真实API或mock）
  2. 计算器工具（安全的eval或手动解析）
  3. 时间/日期工具（datetime模块）

**下午（3h）：完整Agent v1.0**
- [ ] 将Day 3的ReAct Agent + Day 4的工具整合
- [ ] 增加错误处理和重试机制
- [ ] 增加对话记忆（Memory）：用列表存储历史对话
- [ ] 测试Agent能否正确选择工具、处理工具调用失败
- [ ] **产出**：推送代码到GitHub，写README.md（中英文都写）

**资源**：
- OpenAI Function Calling文档: https://platform.openai.com/docs/guides/function-calling
- DeepSeek也支持Function Calling，API格式兼容

---

## 📅 Day 5-6：框架实战（LangChain + RAG）

### Day 5（6小时）：LangChain入門

> 广州JD里「熟练使用LangChain/LangGraph」是硬性要求

**上午（3h）：LangChain核心概念**
- [ ] Chain：最简单的LLMChain → SequentialChain
- [ ] Tool：如何用`@tool`装饰器定义工具
- [ ] Agent：`create_react_agent` + `AgentExecutor`
- [ ] Memory：`ConversationBufferMemory`、`ConversationSummaryMemory`
- [ ] **练习**：用LangChain重写Day 4的手写Agent

**下午（3h）：LangGraph基础**
- [ ] 理解图（Graph）概念：节点（Node）和边（Edge）
- [ ] State：如何在节点间传递状态
- [ ] 条件边（Conditional Edge）：根据结果走不同分支
- [ ] **练习**：用LangGraph实现一个多步骤Agent
  - 场景：用户问"帮我分析一下广州今天的天气，并推荐穿什么"
  - 步骤：查天气 → 分析温度 → 推荐穿搭

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class AgentState(TypedDict):
    messages: list
    weather: str
    recommendation: str

# 定义节点函数
def get_weather(state):
    # 查询天气
    return {"weather": "今天广州28°C，多云"}

def analyze_and_recommend(state):
    # 根据天气推荐
    weather = state["weather"]
    # ...调用LLM分析
    return {"recommendation": "建议穿短袖，带薄外套"}

# 构建图
graph = StateGraph(AgentState)
graph.add_node("get_weather", get_weather)
graph.add_node("recommend", analyze_and_recommend)
graph.add_edge("get_weather", "recommend")
graph.add_edge("recommend", END)
graph.set_entry_point("get_weather")
app = graph.compile()
```

---

### Day 6（6小时）：RAG（检索增强生成）

> 广州JD中「熟悉RAG架构、向量数据库」是核心加分项

**上午（3h）：RAG原理 + 基础实现**
- [ ] RAG是什么？为什么要RAG？（解决幻觉、知识更新、领域知识）
- [ ] RAG完整链路：
  - Document Loading → Text Splitting → Embedding → Vector Store → Retrieval → Generation
- [ ] Embedding：文本怎么变成向量？（用DeepSeek或OpenAI的embedding API）
- [ ] 向量数据库：Chroma（轻量，适合学习）
- [ ] **练习**：搭建一个"个人知识库问答系统"
  - 把你的一些笔记/文章切成chunk → 向量化 → 存入Chroma → 检索 → 回答

**下午（3h）：RAG进阶 + 完整Agent v2.0**
- [ ] 混合检索：关键词检索 + 向量检索
- [ ] Query改写：用户问"那个东西怎么样"→ 改写为"XX产品怎么样"
- [ ] **整合项目**：RAG + Agent = 知识库Agent
  - 用户上传PDF → Agent自动读取 → 存入向量库 → 用户可提问 → Agent检索并回答
  - 用LangChain的`PyPDFLoader` + `RecursiveCharacterTextSplitter` + `Chroma` + `OpenAIEmbeddings`

**资源**：
- LangChain官方文档: https://python.langchain.com/docs/
- Chroma文档: https://docs.trychroma.com/
- LlamaIndex（LangChain的替代品，也可以了解）: https://docs.llamaindex.ai/

---

## 📅 Day 7-8：完整项目冲刺

### Day 7（7小时）：GitHub作品集项目

> 广州JD里「GitHub有完整AI开源项目」是通关密码

**全天：搭建「AI简历分析 + 面试助手 Agent」**

这是你面试时展示的核心项目，功能包括：
1. 用户上传PDF简历 → Agent解析
2. Agent分析简历亮点和不足
3. 针对目标岗位生成面试问题
4. 用户回答问题后，Agent给出改进建议

**技术栈**：
- PDF解析：PyPDFLoader (LangChain)
- LLM：DeepSeek API
- Agent框架：LangChain / LangGraph
- RAG：Chroma向量数据库存储面试题库
- 前端：Gradio（最简单的Python Web UI）
- 部署：本地可运行即可

**项目结构**：
```
resume-agent/
├── README.md          # 中英文，写清楚功能、技术栈、如何运行
├── requirements.txt   # 依赖列表
├── main.py           # Gradio入口
├── agent.py          # Agent核心逻辑
├── tools.py          # 工具定义（PDF解析、搜索等）
├── rag.py            # RAG相关（向量存储、检索）
├── prompts.py        # Prompt模板
└── demo.png          # 效果截图
```

---

### Day 8（7小时）：项目完善 + 第二项目

**上午（3.5h）：完善Day 7项目**
- [ ] 写好README（非常重要！面试官第一眼就看这个）
- [ ] 录制一个30秒的demo GIF/screenshot
- [ ] 处理边界情况（PDF格式错误、超大文件等）
- [ ] 代码注释和文档字符串
- [ ] 推送到GitHub，设为Public

**下午（3.5h）：第二个项目（加分项）**
选择以下之一：
- **方案A**：用Coze/Dify搭建一个低代码Agent（体现多平台能力）
- **方案B**：多Agent协作demo（如：一个研究员Agent + 一个写手Agent协作写报告）
- **方案C**：用FastAPI把Day 7的项目部署成API服务 + 简单前端

**产出**：2个GitHub仓库 + 1个Coze/Dify Bot

---

## 📅 Day 9-10：面试冲刺 + 投递

### Day 9（6小时）：技术八股 + 简历

**上午（3h）：Agent面试高频题准备**

必背题目清单：
1. **「Agent的核心架构是什么？」** → Planning + Memory + Tools + Action（每个展开2-3句）
2. **「ReAct模式和普通的Chain有什么区别？」** → ReAct有观察-思考循环，Chain是线性的
3. **「LangChain的Agent和直接调API有什么区别？」** → LangChain提供了工具管理、记忆管理、错误重试等工程化能力
4. **「RAG的完整流程是什么？有哪些优化点？」** → 加载→切分→向量化→存储→检索→生成；优化：Query改写、混合检索、重排
5. **「多Agent之间怎么通信和隔离？」** → 消息传递、共享记忆、工具隔离、Prompt隔离
6. **「Function Calling的原理？」** → 模型输出JSON → 程序解析 → 执行函数 → 结果返回模型
7. **「你做的项目里最大的挑战是什么？怎么解决的？」** → 准备1-2个真实的故事
8. **「向量数据库的原理？为什么不用传统数据库？」** → 高维向量相似度搜索（ANN），传统数据库无法高效做语义搜索

**下午（3h）：简历打磨**
- [ ] 用LaTeX或Canva做一份简洁专业的简历
- [ ] 必须包含：
  - 教育背景（硕士+本科，专业GPA如果高就写）
  - **项目经历**（放最前面！2个项目各3-4条bullet point）
  - 技术栈（Python, LangChain, LangGraph, RAG, LLM, FastAPI, Git等）
  - GitHub链接（必须放！）
- [ ] 简历检查清单：
  - 一页纸
  - 每个项目用STAR法则（情境-任务-行动-结果）
  - 量化结果（如：实现XX功能，准确率提升XX%）
  - 没有错别字

**资源**：
- 超级简历: https://www.wondercv.com/
- Overleaf LaTeX简历模板: https://www.overleaf.com/latex/templates/tagged/cv

---

### Day 10（6小时）：模拟面试 + 开始投递

**上午（2h）：模拟面试**
- [ ] 用DeepSeek或Claude模拟一轮Agent岗技术面
  - 让它扮演面试官，按广州JD要求提问
  - 你用中文回答，然后让它打分+给建议
- [ ] 重点练：
  - 自我介绍（30秒版 + 2分钟版）
  - 项目介绍（从业务场景讲到技术实现）
  - 手撕代码（准备3-5道LeetCode中等题）

**技巧——项目介绍的6种讲法**：
| 版本 | 时长 | 内容重点 |
|------|------|----------|
| 一句话版 | 10秒 | "我做了个简历分析Agent，用LangChain+RAG，能自动解析PDF并生成面试建议" |
| 电梯演讲 | 30秒 | 加上解决了什么问题、用了什么技术 |
| 展开版 | 2分钟 | 加上架构设计、技术选型理由 |
| 技术深挖版 | 5分钟 | 加上具体实现细节、遇到的坑 |
| 业务价值版 | 2分钟 | 加上这个项目能带来什么价值 |
| 反思版 | 2分钟 | 加上如果重做会怎么改进 |

**下午（2h）：正式投递**
- [ ] 平台注册+完善资料：
  - BOSS直聘、拉勾、实习僧、牛客网
  - LinkedIn（阿科玛等外企需要）
- [ ] 搜索关键词：`AI Agent` `大模型` `智能体` `RAG` `LLM` `LangChain` `广州 实习`
- [ ] 每天投10-20家，不要只投Agent，相关方向也投（NLP、大模型应用、后端开发）
- [ ] 准备一段私信模板（BOSS直聘上打招呼用）

**投递话术模板**：
```
您好，我是XX大学AI专业研一学生，对贵司的[岗位名称]非常感兴趣。

我有Python+LangChain+Agent开发经验，独立完成了2个AI Agent项目：
1. [项目1名称+一句话描述]
2. [项目2名称+一句话描述]

项目代码在GitHub：[链接]
希望能有机会进一步沟通，谢谢！
```

**晚上（2h）：复盘 + 持续学习计划**
- [ ] 整理一份面试问题清单（把面试中遇到的问题记下来）
- [ ] 制定投递后的持续学习计划（每天保持2-3小时学习）

---

## 🛠️ 工具清单（全部免费/低成本）

| 类别 | 工具 | 用途 |
|------|------|------|
| LLM API | DeepSeek API | 主力模型，便宜好用 |
| Agent框架 | LangChain + LangGraph | 工程化开发 |
| 向量数据库 | Chroma | RAG项目 |
| 低代码平台 | Coze(扣子) / Dify | 快速验证想法 |
| IDE | VS Code + GitHub Copilot(学生免费) | 写代码 |
| 版本管理 | Git + GitHub | 作品集展示 |
| 笔记 | Obsidian / Notion | 学习笔记 |
| 面试刷题 | LeetCode(只刷Hot100) | 算法面试 |

---

## ⚠️ 注意事项

1. **不要死磕原理**：10天的目标不是成为专家，是「能做出东西 + 能讲清楚」
2. **代码 > 理论**：每天至少50%时间在写代码，不要只看视频/文章
3. **GitHub绿点**：从Day 1开始每天push代码，面试官会看你的contribution graph
4. **不会就问AI**：用Claude/DeepSeek当你的24小时助教，卡住了就问
5. **海投策略**：广州Agent岗可能不超过50个，相关方向（NLP、大模型应用、Python后端）也投
6. **没有回复很正常**：应届生海投回复率5-10%是正常的，投100家拿5-10个面试就是胜利

---

## 📈 10天后的持续学习路线

如果10天投递后需要边面试边继续学习：

| 周期 | 学习内容 | 目标 |
|------|----------|------|
| 第3-4周 | FastAPI+Docker部署、多Agent系统（CrewAI/AutoGen） | 能部署上线的完整系统 |
| 第5-6周 | 模型微调（LoRA/QLoRA）、MCP协议、Agent评测 | 深入底层能力 |
| 第7-8周 | 看论文（ReAct/ AutoGPT/ MetaGPT最新进展） | 面试能聊前沿 |

---

> **最后一句**：10天后你不需要成为专家，你只需要比同样找实习的人多2个GitHub项目 + 能用嘴说出Agent是怎么回事。这就够了。加油🔥
