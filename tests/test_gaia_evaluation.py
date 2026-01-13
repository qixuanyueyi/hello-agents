# test_gaia_evaluation.py
"""
GAIA (General AI Assistants) 评估工具测试
用于测试智能体在GAIA基准上的表现
"""
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
load_dotenv()

from hello_agents import SimpleAgent, HelloAgentsLLM
from hello_agents.tools import GAIAEvaluationTool

# GAIA官方系统提示词（来自论文）
GAIA_SYSTEM_PROMPT = """You are a general AI assistant. I will ask you a question. Report your thoughts, and finish your answer with the following template: FINAL ANSWER: [YOUR FINAL ANSWER].

YOUR FINAL ANSWER should be a number OR as few words as possible OR a comma separated list of numbers and/or strings.

If you are asked for a number, don't use comma to write your number neither use units such as $ or percent sign unless specified otherwise.

If you are asked for a string, don't use articles, neither abbreviations (e.g. for cities), and write the digits in plain text unless specified otherwise.

If you are asked for a comma separated list, apply the above rules depending of whether the element to be put in the list is a number or a string."""

# 1. 创建智能体（使用GAIA官方系统提示词）
print("=== 初始化智能体 ===")
llm = HelloAgentsLLM()
agent = SimpleAgent(
    name="TestAgent",
    llm=llm,
    system_prompt=GAIA_SYSTEM_PROMPT  # 关键：使用GAIA官方提示词
)

# 2. 创建GAIA评估工具
print("=== 创建GAIA评估工具 ===")
gaia_tool = GAIAEvaluationTool()

# 3. 一键运行评估
print("=== 开始GAIA评估 ===")
results = gaia_tool.run(
    agent=agent,
    level=1,  # Level 1: 简单任务
    max_samples=5,  # 评估5个样本
    export_results=True,  # 导出GAIA格式结果
    generate_report=True  # 生成评估报告
)

# 4. 查看结果
print("\n=== 评估结果 ===")
print(f"精确匹配率: {results['exact_match_rate']:.2%}")
print(f"部分匹配率: {results['partial_match_rate']:.2%}")
print(f"正确数: {results['exact_matches']}/{results['total_samples']}")

# 可选：查看详细信息
if 'samples' in results:
    print("\n=== 样本详情 ===")
    for i, sample in enumerate(results.get('samples', [])[:3]):  # 只显示前3个
        print(f"\n样本 {i+1}:")
        print(f"  问题: {sample.get('question', 'N/A')[:80]}...")
        print(f"  预期答案: {sample.get('expected', 'N/A')}")
        print(f"  模型答案: {sample.get('predicted', 'N/A')}")
        print(f"  是否正确: {'✓' if sample.get('exact_match') else '✗'}")
