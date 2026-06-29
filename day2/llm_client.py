"""
Day 2 核心文件：DeepSeek LLM 客户端封装

学完这个文件你就能理解：
1. 如何用 Python 调用大模型 API
2. System Prompt 如何影响模型行为
3. Temperature 如何控制输出创造性
4. 如何封装成可复用的类（面试官会看你的代码组织能力）
"""

import requests
import json
import os
from typing import Optional, List, Dict


class DeepSeekClient:
    """
    DeepSeek API 的 Python 封装。

    使用方式：
        client = DeepSeekClient(api_key="sk-xxx")
        answer = client.chat("用Python写一个快速排序")
        print(answer)

    面试要点：为什么封装成类？
    → 统一管理 API Key、默认参数、错误处理
    → 后续写 Agent 时，Agent 直接持有 client 实例即可，不用每次都传 key
    """

    # DeepSeek API 的基础地址（兼容 OpenAI 格式）
    BASE_URL = "https://api.deepseek.com/v1/chat/completions"

    def __init__(self, api_key: str = None, default_model: str = "deepseek-chat"):
        """
        初始化客户端。

        参数：
            api_key: DeepSeek API Key。如果传 None，会自动尝试从环境变量
                     DEEPSEEK_API_KEY 或文件 .deepseek_key 读取。
            default_model: 默认使用的模型名称。
                           - deepseek-chat: 通用对话（便宜，够用）
                           - deepseek-reasoner: 推理增强版（贵一些，数学/逻辑更强）
        """
        self.api_key = api_key or self._load_api_key()
        self.default_model = default_model
        self.last_response = None  # 保留最近一次完整响应，方便调试

    # ------------------------------------------------------------------
    # 公开方法
    # ------------------------------------------------------------------

    def chat(
        self,
        user_message: str,
        system_prompt: str = "你是一个有用的AI助手。",
        temperature: float = 0.7,
        model: str = None,
        max_tokens: int = 2048,
        history: List[Dict] = None,
    ) -> str:
        """
        发送一次对话，返回模型的文本回复。

        参数：
            user_message:  用户说的话
            system_prompt: 系统提示词——定义模型的"人设"和行为规则
            temperature:   创造性参数。0=确定，1.5=天马行空
            model:         模型名，不传则用默认的 deepseek-chat
            max_tokens:    回复的最大长度（token 数）
            history:       历史对话记录，格式：[{"role":"user","content":"..."}, ...]

        返回：
            模型回复的文本内容

        面试要点：system_prompt 是 Agent 控制模型行为的核心手段，
                 后面写 ReAct Agent 时会大量用到。
        """
        # 1. 构建消息列表
        messages = self._build_messages(user_message, system_prompt, history)

        # 2. 发送请求
        response_data = self._call_api(messages, temperature, model or self.default_model, max_tokens)

        # 3. 提取文本回复
        try:
            content = response_data["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as e:
            # 出错时打印完整响应用于调试
            print(f"[ERROR] 解析响应失败: {e}")
            print(f"[DEBUG] 完整响应: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
            raise

        return content

    def chat_with_stream(self, user_message: str, system_prompt: str = "你是一个有用的AI助手。",
                         temperature: float = 0.7, model: str = None) -> str:
        """
        流式对话——逐字打印，像 ChatGPT 网页版一样。

        面试要点：stream=True 能让用户体验更好（不用等全部生成完才能看到内容），
                 但 Agent 内部调用通常不用流式（需要完整文本才能解析下一步动作）。
        """
        messages = self._build_messages(user_message, system_prompt)

        payload = {
            "model": model or self.default_model,
            "messages": messages,
            "temperature": temperature,
            "stream": True,
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        response = requests.post(
            self.BASE_URL,
            headers=headers,
            json=payload,
            stream=True,
            timeout=60,
        )
        response.raise_for_status()

        full_content = ""
        print("🤖 ", end="", flush=True)
        for line in response.iter_lines():
            if not line:
                continue
            line_str = line.decode("utf-8")
            if line_str.startswith("data: "):
                data_str = line_str[6:]
                if data_str.strip() == "[DONE]":
                    break
                try:
                    chunk = json.loads(data_str)
                    delta = chunk["choices"][0].get("delta", {})
                    content = delta.get("content", "")
                    if content:
                        print(content, end="", flush=True)
                        full_content += content
                except json.JSONDecodeError:
                    continue
        print()  # 换行
        return full_content

    # ------------------------------------------------------------------
    # 内部方法（前缀 _ 表示"私有"，外部不需要关心）
    # ------------------------------------------------------------------

    def _build_messages(
        self, user_message: str, system_prompt: str, history: List[Dict] = None
    ) -> List[Dict]:
        """构建完整的 messages 列表。"""
        messages = [{"role": "system", "content": system_prompt}]

        # 如果有历史对话，追加进去（Agent 的 Memory 就是这么实现的！）
        if history:
            messages.extend(history)

        messages.append({"role": "user", "content": user_message})
        return messages

    def _call_api(
        self, messages: List[Dict], temperature: float, model: str, max_tokens: int
    ) -> Dict:
        """发送 HTTP POST 请求到 DeepSeek API。"""
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False,
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        response = requests.post(self.BASE_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()  # 如果 HTTP 状态码不是 2xx，抛出异常

        self.last_response = response.json()
        return self.last_response

    @staticmethod
    def _load_api_key() -> str:
        """
        尝试多种方式加载 API Key（优先级从高到低）：
        1. 环境变量 DEEPSEEK_API_KEY
        2. 项目目录下的 .deepseek_key 文件
        3. 都没有 → 抛异常，提示用户去注册
        """
        # 方式1：环境变量
        key = os.environ.get("DEEPSEEK_API_KEY")
        if key:
            return key

        # 方式2：本地文件（不要提交到 Git！）
        key_file = os.path.join(os.path.dirname(__file__), "..", ".deepseek_key")
        if os.path.exists(key_file):
            with open(key_file, "r", encoding="utf-8") as f:
                return f.read().strip()

        raise ValueError(
            "未找到 DeepSeek API Key！请以下任一方式提供：\n"
            "  1. 设置环境变量: export DEEPSEEK_API_KEY=sk-xxx\n"
            "  2. 在项目根目录创建 .deepseek_key 文件，粘贴你的 API Key\n"
            "  3. 代码中直接传入: DeepSeekClient(api_key='sk-xxx')\n\n"
            "  去 https://platform.deepseek.com/ 注册并获取 Key（新用户送500万token）"
        )


# ======================================================================
# 快速测试（直接运行此文件时执行）
# ======================================================================
if __name__ == "__main__":
    import sys

    # 优先用命令行参数，否则从环境变量/文件读取
    api_key = sys.argv[1] if len(sys.argv) > 1 else None

    try:
        client = DeepSeekClient(api_key=api_key)
    except ValueError as e:
        print(e)
        sys.exit(1)

    # 测试默认对话
    print("=" * 60)
    print("测试 1：默认对话（temperature=0.7）")
    print("=" * 60)
    result = client.chat("用一句话解释什么是 Python 装饰器")
    print(f"🤖 {result}")
    print()

    # 测试低 temperature（更确定）
    print("=" * 60)
    print("测试 2：低温度（temperature=0.1，更确定）")
    print("=" * 60)
    result = client.chat(
        "1 + 1 等于几？只回答数字。",
        temperature=0.1,
    )
    print(f"🤖 {result}")
    print()

    # 测试高 temperature（更有创造性）
    print("=" * 60)
    print("测试 3：高温度（temperature=1.5，更有创造性）")
    print("=" * 60)
    result = client.chat(
        "给一家AI创业公司起3个名字，要中文的，有创意。",
        temperature=1.5,
    )
    print(f"🤖 {result}")
