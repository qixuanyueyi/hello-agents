# test_gaia_dataset.py
"""
GAIA (General AI Assistants) 数据集加载测试
用于加载和测试GAIA基准测试数据
"""
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
load_dotenv()

from hello_agents.evaluation import GAIADataset

# 自动从.env读取HF_TOKEN，或手动设置:
# import os
# os.environ["HF_TOKEN"] = "hf_your_token_here"

# 自动下载到 ./data/gaia/
dataset = GAIADataset(
    dataset_name="gaia-benchmark/GAIA",
    split="validation",  # 或 "test"
    level=1  # 可选: 1, 2, 3, None(全部)
)
items = dataset.load()

print(f"加载了 {len(items)} 个测试样本")
# 输出: 加载了 53 个测试样本 (Level 1)

# 可选: 查看示例数据
if items:
    print("\n=== 示例样本 ===")
    sample = items[0]
    print(f"问题: {sample.get('question', 'N/A')[:100]}...")
