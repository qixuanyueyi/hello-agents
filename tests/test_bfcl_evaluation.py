# test_bfcl_evaluation.py
"""
BFCL (Berkeley Function Calling Leaderboard) 评估工具测试
用于测试智能体的函数调用能力
"""
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
from hello_agents import SimpleAgent, HelloAgentsLLM
from hello_agents.tools import BFCLEvaluationTool

# 加载环境变量
load_dotenv()

# 1. 创建要评估的智能体
print("=== 初始化LLM和Agent ===")
llm = HelloAgentsLLM()
agent = SimpleAgent(name="TestAgent", llm=llm)

# 2. 创建BFCL评估工具
print("=== 创建BFCL评估工具 ===")
bfcl_tool = BFCLEvaluationTool()

# 3. 运行评估（自动完成所有步骤）
print("=== 开始BFCL评估 ===")
results = bfcl_tool.run(
    agent=agent,
    category="simple_python",  # 评估类别
    max_samples=5              # 评估样本数（0表示全部）
)

# 4. 查看结果
print("\n=== 评估结果 ===")
print(f"准确率: {results['overall_accuracy']:.2%}")
print(f"正确数: {results['correct_samples']}/{results['total_samples']}")

# 可选：查看详细评估指标
if 'detailed_metrics' in results:
    print("\n=== 详细指标 ===")
    for metric_name, metric_value in results.get('detailed_metrics', {}).items():
        print(f"  {metric_name}: {metric_value}")
