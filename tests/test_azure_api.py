import os
from dotenv import load_dotenv
# 加载环境变量（确保在项目根目录有.env文件）
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

# 绝对导入（因为 pip install -e . 已注册 hello_agents 包）
from hello_agents.agents import SimpleAgent  
from hello_agents.core import HelloAgentsLLM
from hello_agents.tools import CalculatorTool

# 测试函数（pytest 识别以 test_ 开头的函数）
def test_agent_basic():
    # 创建 LLM 和 Agent
    llm = HelloAgentsLLM()
    agent = SimpleAgent(name="AI助手", llm=llm, system_prompt="你是一个有用的AI助手")
    
    # 测试基础对话
    response = agent.run("你好！请介绍一下自己")
    assert response is not None  # 断言响应非空
    print("基础对话响应：", response)
    
    # 测试工具调用（如果后续支持）
    # calculator = CalculatorTool()
    # agent.add_tool(calculator)
    # calc_response = agent.run("计算 2 + 3 * 4")
    # assert "14" in calc_response

# 可选：直接运行测试（兼容手动执行）
if __name__ == "__main__":
    test_agent_basic()