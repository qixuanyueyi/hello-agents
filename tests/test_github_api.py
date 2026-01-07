import time
import pytest
from dotenv import load_dotenv

# 加载项目根目录的 .env 文件
load_dotenv()  # 默认加载当前目录及父目录的 .env 文件

from hello_agents.tools import MCPTool


@pytest.fixture 
def github_tool():
    """创建 GitHub MCP 工具的 fixture"""
    tool = MCPTool(
        server_command=["npx", "-y", "@modelcontextprotocol/server-github"]
    )
    yield tool
    # 清理资源
    time.sleep(0.5)


def test_list_tools(github_tool):
    """测试列出可用工具"""
    print("\n📋 测试列出可用工具...")
    result = github_tool.run({"action": "list_tools"})
    print(result)
    
    assert result is not None
    assert "工具" in result or "tool" in result.lower()


def test_search_repositories(github_tool):
    """测试搜索仓库"""
    print("\n🔍 测试搜索仓库...")
    result = github_tool.run({
        "action": "call_tool",
        "tool_name": "search_repositories",
        "arguments": {
            "query": "AI agents language:python",
            "page": 1,
            "perPage": 3
        }
    })
    print(result)
    
    assert result is not None
    assert "search_repositories" in result


if __name__ == "__main__":
    # 直接运行此文件时的行为
    pytest.main([__file__, "-v"])