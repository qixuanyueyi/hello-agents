from hello_agents import SimpleAgent, HelloAgentsLLM, ToolRegistry
from hello_agents.tools import MemoryTool

from dotenv import load_dotenv
# 加载项目根目录的 .env 文件
load_dotenv()  # 默认加载当前目录及父目录的 .env 文件

# 创建具有记忆能力的Agent
llm = HelloAgentsLLM()
agent = SimpleAgent(name="记忆助手", llm=llm)

# 创建记忆工具
memory_tool = MemoryTool(user_id="user123")
tool_registry = ToolRegistry()
tool_registry.register_tool(memory_tool)
agent.tool_registry = tool_registry
 
# 体验记忆功能
print("=== 添加多个记忆 ===")

# 添加第一个记忆
result1 = memory_tool.run(
    parameters={
        "action": "add",  # 必需参数：指定要执行的操作
        "content": "用户张三是一名Python开发者，专注于机器学习和数据分析",
        "memory_type": "semantic",
        "importance": 0.8
        # 可选参数（如果需要可以加）：file_path、modality
    }
)
print(f"记忆1: {result1}")

# 添加第二个记忆
result2 = memory_tool.run(
    parameters={
        "action": "add",
        "content": "李四是一名前端工程师，擅长React和Vue框架开发",
        "memory_type": "semantic",
        "importance": 0.7
    }
)
print(f"记忆2: {result2}")

# 添加第三个记忆
result3 = memory_tool.run(
    parameters={
        "action": "add",
        "content": "王五是产品经理，负责用户体验设计和需求分析",
        "memory_type": "semantic",
        "importance": 0.6
    }
)
print(f"记忆3: {result3}")

print("\n=== 搜索特定记忆 ===")
# 搜索包含“王五”的记忆
print("🔍 搜索 '王五':")
result = memory_tool.run(
    parameters={
        "action": "search",
        "query": "王五",
        "memory_type": "semantic",
        "top_k": 2
    }
)
print(result)

print("\n=== 记忆摘要 ===")
result = memory_tool.run(
    parameters={
        "action": "summary"
    }
)
print(result)