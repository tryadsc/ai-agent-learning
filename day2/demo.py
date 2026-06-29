"""
Day 2 实验脚本：感受 System Prompt 和 Temperature 的魔力

这个脚本会依次演示：
1. 同一个问题 + 不同 System Prompt → 完全不同的回答风格
2. 同一个问题 + 不同 Temperature → 从"死板"到"创意"
3. 多轮对话（用 history 参数实现 Memory）

运行方式：
    python day2/demo.py

确保你已经配置了 API Key（参考 llm_client.py 里的三种方式）。
"""

from llm_client import DeepSeekClient


def section(title: str):
    """打印分隔线，让输出更好看。"""
    print()
    print("=" * 65)
    print(f"  {title}")
    print("=" * 65)


def demo_1_system_prompt(client: DeepSeekClient):
    """
    实验1：System Prompt 如何塑造模型行为

    核心理解：
    - System Prompt = 模型的"人设说明书"
    - 同样的 User Prompt，不同 System Prompt → 输出完全不同
    - Agent 开发中，System Prompt 是最核心的控制手段
    """
    section("实验 1：System Prompt 的魔法")

    question = "请解释什么是机器学习。"

    # Persona A：大学教授
    answer_a = client.chat(
        user_message=question,
        system_prompt="你是一位严谨的计算机科学教授。请用学术风格回答，引用关键概念和术语。",
        temperature=0.3,
    )

    # Persona B：幼儿园老师
    answer_b = client.chat(
        user_message=question,
        system_prompt="你是一位幼儿园老师。请用5岁小朋友能听懂的方式解释，可以用类比和故事。",
        temperature=0.7,
    )

    # Persona C：只说英文
    answer_c = client.chat(
        user_message=question,
        system_prompt="You are a helpful assistant. You ONLY reply in English, no matter what language the user uses.",
        temperature=0.7,
    )

    # Persona D：代码示例优先
    answer_d = client.chat(
        user_message=question,
        system_prompt="你是一个实战派程序员导师。回答任何技术问题都要附带可运行的Python代码示例。",
        temperature=0.5,
    )

    print(f"\n📝 问题：{question}")
    print(f"\n--- 👨‍🏫 人设A：大学教授 ---")
    print(answer_a[:500])
    print(f"\n--- 👶 人设B：幼儿园老师 ---")
    print(answer_b[:500])
    print(f"\n--- 🇬🇧 人设C：只说英文 ---")
    print(answer_c[:300])
    print(f"\n--- 💻 人设D：代码示例优先 ---")
    print(answer_d[:500])

    print("\n💡 要点：System Prompt 是 Agent 的「灵魂」，后面写 Agent 时会用它来定义")
    print("   Agent 的行为规则：什么情况用什么工具、如何思考、输出什么格式。")


def demo_2_temperature(client: DeepSeekClient):
    """
    实验2：Temperature 如何影响输出

    核心理解：
    - 低 temperature → 模型选最高概率的词 → 输出稳定但无聊
    - 高 temperature → 模型有概率选"不那么可能"的词 → 输出多样但可能跑偏
    - 代码/数学/事实问答 → 低温度；创意/写作/取名 → 高温度
    """
    section("实验 2：Temperature 的调参实验")

    question = "写一首关于广州夏天的五言绝句。"

    temperatures = [0.0, 0.3, 0.7, 1.0, 1.5]

    for temp in temperatures:
        answer = client.chat(
            user_message=question,
            system_prompt="你是一个诗人。",
            temperature=temp,
        )
        print(f"\n🌡️  Temperature = {temp}")
        print(f"   {answer.strip()[:200]}")

    print("\n💡 要点：")
    print("   - temp=0.0：每次都一样（完全确定）")
    print("   - temp=0.7：有一定变化，但还靠谱")
    print("   - temp=1.5：可能有意想不到的表达，也可能跑偏")


def demo_3_multi_turn(client: DeepSeekClient):
    """
    实验3：多轮对话（Memory 的基础）

    核心理解：
    - LLM 本身是「无状态」的——每次调用都是全新开始
    - 要让模型"记住"之前说了什么，需要把历史对话传回去
    - 这就是 Agent Memory 的最基础实现方式！
    - Day 1 写的 Memory 类就是为了干这个
    """
    section("实验 3：多轮对话——Memory 的基础")

    # 模拟一段对话历史
    history = []

    # 第一轮
    reply1 = client.chat(
        user_message="我叫小明，我正在学 Python。",
        system_prompt="你是一个编程助教。请用中文回答。",
        temperature=0.7,
    )
    print(f"\n👤 用户：我叫小明，我正在学 Python。")
    print(f"🤖 助教：{reply1.strip()[:200]}")
    history.append({"role": "user", "content": "我叫小明，我正在学 Python。"})
    history.append({"role": "assistant", "content": reply1})

    # 第二轮：模型能记住"小明"吗？
    reply2 = client.chat(
        user_message="我刚才说我叫什么名字？我在学什么？",
        system_prompt="你是一个编程助教。请用中文回答。",
        temperature=0.7,
        history=history,  # ← 关键！把历史传回去
    )
    print(f"\n👤 用户：我刚才说我叫什么名字？我在学什么？")
    print(f"🤖 助教：{reply2.strip()[:200]}")

    # 第三轮：不带 history 试试看（模型会"失忆"）
    reply3 = client.chat(
        user_message="我叫什么名字？",
        system_prompt="你是一个编程助教。请用中文回答。",
        temperature=0.7,
        # 注意：这里故意不传 history！
    )
    print(f"\n👤 用户（不带 history）：我叫什么名字？")
    print(f"🤖 助教（失忆版）：{reply3.strip()[:200]}")

    print("\n💡 要点：")
    print("   - 带了 history → 模型记得之前说过的一切")
    print("   - 没带 history → 模型完全「失忆」，不知道你是谁")
    print("   - Agent 的 Memory 本质上就是把历史对话存起来，每次传给 LLM")


def demo_4_api_params(client: DeepSeekClient):
    """
    实验4：认识 API 请求/响应的完整结构

    面试常见追问：「API 请求体里有哪些关键字段？」
    看完这个你就知道了。
    """
    section("实验 4：API 请求和响应的完整结构")

    # 发一个请求，然后查看完整的响应
    client.chat(
        user_message="用 Python 写一个 Hello World",
        system_prompt="你是一个代码助手。",
        temperature=0.3,
    )

    # last_response 保存了 DeepSeek 返回的完整 JSON
    import json
    print("\n📦 DeepSeek API 完整响应结构：")
    print(json.dumps(client.last_response, ensure_ascii=False, indent=2)[:1500])

    print("\n💡 响应中包含的关键信息：")
    response = client.last_response
    print(f"   - model: {response.get('model')}")
    print(f"   - 消耗 token 数: {response.get('usage', {})}")
    print(f"   - finish_reason: {response['choices'][0].get('finish_reason')}")


# ======================================================================
# 主程序
# ======================================================================
def main():
    print("🎯 Day 2 实验：LLM API 实战")
    print("   让我们直观感受 System Prompt、Temperature 和多轮对话的效果\n")

    # 初始化客户端
    try:
        client = DeepSeekClient()
    except ValueError as e:
        print(f"❌ {e}")
        print("\n💡 快速解决：在项目根目录创建 .deepseek_key 文件，粘贴你的 API Key")
        return

    # 依次运行 4 个实验
    demo_1_system_prompt(client)
    demo_2_temperature(client)
    demo_3_multi_turn(client)
    demo_4_api_params(client)

    section("🎉 Day 2 实验完成！")
    print("你已经掌握了：")
    print("  ✅ System Prompt 如何控制模型行为")
    print("  ✅ Temperature 如何调节创造性")
    print("  ✅ 多轮对话如何实现（Memory 基础）")
    print("  ✅ API 请求/响应的完整结构")
    print()
    print("📌 记得把代码 push 到 GitHub！面试官看贡献图。")
    print("   git add day2/ && git commit -m \"Day 2: LLM API实战\" && git push")


if __name__ == "__main__":
    main()
