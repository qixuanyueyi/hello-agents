"""测试本地 MCP 工具（内置计算器服务器）"""

import pytest
from dotenv import load_dotenv

# 加载项目根目录的 .env 文件
load_dotenv()

from hello_agents import SimpleAgent, HelloAgentsLLM
from hello_agents.tools import MCPTool


@pytest.fixture
def mcp_tool():
    """创建 MCP 工具的 fixture"""
    return MCPTool(name="calculator")


@pytest.fixture
def agent_with_mcp(mcp_tool):
    """创建带有 MCP 工具的 agent fixture"""
    agent = SimpleAgent(name="助手", llm=HelloAgentsLLM())
    agent.add_tool(mcp_tool)
    return agent


def test_mcp_tool_initialization():
    """测试 MCP 工具初始化"""
    mcp_tool = MCPTool(name="calculator")
    
    assert mcp_tool is not None
    assert mcp_tool.name == "calculator"
    print(f"\n✅ MCP工具 '{mcp_tool.name}' 初始化成功")


def test_mcp_tool_list_tools():
    """测试列出 MCP 工具"""
    mcp_tool = MCPTool(name="calculator")
    
    result = mcp_tool.run({"action": "list_tools"})
    print(f"\n📋 可用工具:\n{result}")
    
    assert result is not None
    assert "工具" in result


def test_mcp_tool_with_agent(agent_with_mcp):
    """测试 MCP 工具与智能体集成"""
    agent = agent_with_mcp
    
    # 验证工具已添加
    tools = agent.list_tools()
    assert len(tools) > 0
    print(f"\n✅ MCP工具已展开为 {len(tools)} 个独立工具")
    print(f"📋 可用工具: {', '.join(tools)}")


def test_agent_calculation(agent_with_mcp):
    """测试智能体使用 MCP 工具进行计算"""
    agent = agent_with_mcp
    
    # 先查看可用的工具
    tools = agent.list_tools()
    print(f"\n📋 可用工具列表: {tools}")
    
    # 智能体使用展开后的工具
    response = agent.run("使用工具计算 25 乘以 16，工具名称中包含 multiply")
    print(f"\n🤖 Agent 响应: {response}")
    
    assert response is not None
    assert "400" in response or "四百" in response, "应该返回计算结果400"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])