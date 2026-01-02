"""
嵌入模型测试脚本 - 诊断 Embedding 配置问题

直接运行: python diagnose_embedding.py
"""

import os
import sys
from dotenv import load_dotenv

# 添加项目路径（修复：需要添加包含hello_agents包的目录）
current_dir = os.path.dirname(os.path.abspath(__file__))
# 如果当前在 hello_agents/hello_agents/ 目录，需要往上两层
# 如果当前在 hello_agents/ 目录，需要往上一层或当前目录
parent_dir = os.path.dirname(current_dir)

# 检测正确的路径
if os.path.exists(os.path.join(current_dir, "hello_agents")):
    # 当前目录就是项目根目录
    project_root = current_dir
elif os.path.exists(os.path.join(parent_dir, "hello_agents")):
    # 父目录是项目根目录
    project_root = parent_dir
else:
    # 当前在 hello_agents 包内，需要往上
    project_root = parent_dir

if project_root not in sys.path:
    sys.path.insert(0, project_root)

print("="*60)
print("🔍 嵌入模型配置诊断")
print("="*60)
print(f"当前目录: {current_dir}")
print(f"项目根目录: {project_root}")

# 1. 加载 .env 文件
print("\n【步骤1】加载 .env 文件")
# 尝试在多个位置查找 .env
env_paths = [
    os.path.join(project_root, ".env"),
    os.path.join(current_dir, ".env"),
    os.path.join(parent_dir, ".env"),
]

env_path = None
for path in env_paths:
    if os.path.exists(path):
        env_path = path
        break

if env_path:
    load_dotenv(env_path)
    print(f"✅ 找到 .env 文件: {env_path}")
    
    # 显示 .env 内容（隐藏敏感信息）
    print("\n.env 文件内容:")
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                if 'KEY' in line or 'PASSWORD' in line:
                    key = line.split('=')[0]
                    print(f"  {key}=***")
                else:
                    print(f"  {line}")
else:
    print(f"❌ 未找到 .env 文件")
    print(f"尝试过的路径:")
    for path in env_paths:
        print(f"  - {path}")
    print("\n提示: 请在项目根目录创建 .env 文件")
    print("\n示例 .env 内容:")
    print("  EMBED_MODEL_TYPE=dashscope")
    print("  EMBED_MODEL_NAME=text-embedding-v3")
    print("  EMBED_API_KEY=your_api_key_here")

# 2. 检查环境变量
print("\n【步骤2】检查环境变量")
embed_type = os.getenv("EMBED_MODEL_TYPE")
embed_name = os.getenv("EMBED_MODEL_NAME")
embed_key = os.getenv("EMBED_API_KEY")
embed_url = os.getenv("EMBED_BASE_URL")

print(f"EMBED_MODEL_TYPE: {embed_type or '(未设置)'}")
print(f"EMBED_MODEL_NAME: {embed_name or '(未设置)'}")
print(f"EMBED_API_KEY: {embed_key[:20] + '...' if embed_key else '(未设置)'}")
print(f"EMBED_BASE_URL: {embed_url or '(未设置)'}")

# 3. 检查依赖包
print("\n【步骤3】检查依赖包")
packages = {
    "sentence-transformers": "sentence_transformers",
    "transformers": "transformers",
    "torch": "torch",
    "dashscope": "dashscope",
    "scikit-learn": "sklearn",
    "requests": "requests",
}

missing_packages = []
for display_name, import_name in packages.items():
    try:
        mod = __import__(import_name)
        version = getattr(mod, '__version__', '未知版本')
        print(f"✅ {display_name}: 已安装 (v{version})")
    except ImportError:
        print(f"❌ {display_name}: 未安装")
        missing_packages.append(display_name)

# 3.5 检查 hello_agents 模块是否可导入
print("\n【步骤3.5】检查 hello_agents 模块")
try:
    import hello_agents
    print(f"✅ hello_agents 模块可导入")
    print(f"   路径: {hello_agents.__file__}")
except ImportError as e:
    print(f"❌ hello_agents 模块不可导入: {e}")
    print(f"   sys.path: {sys.path[:3]}...")
    print("\n解决方案:")
    print(f"   cd {project_root}")
    print("   pip install -e .")

# 4. 测试各种嵌入模型
print("\n【步骤4】测试嵌入模型")

def test_embedding(model_type: str, **kwargs):
    """测试单个嵌入模型"""
    print(f"\n--- 测试 {model_type.upper()} 模型 ---")
    try:
        from hello_agents.memory.embedding import create_embedding_model
        
        print(f"正在创建模型...")
        model = create_embedding_model(model_type, **kwargs)
        print(f"✅ 模型创建成功: {type(model).__name__}")
        
        # 测试编码
        test_text = "这是一个测试文本"
        print(f"正在编码单个文本...")
        embedding = model.encode(test_text)
        print(f"✅ 编码成功，维度: {len(embedding)}")
        print(f"   向量示例: [{', '.join([f'{x:.4f}' for x in embedding[:5]])}...]")
        
        # 测试批量编码
        test_texts = ["文本1", "文本2", "文本3"]
        print(f"正在批量编码 {len(test_texts)} 个文本...")
        embeddings = model.encode(test_texts)
        print(f"✅ 批量编码成功，数量: {len(embeddings)}")
        
        return True
    except Exception as e:
        print(f"❌ 失败: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

# 4.1 测试 DashScope
dashscope_success = False
if embed_type == "dashscope" or not embed_type:
    print("\n🔵 准备测试 DashScope 模型")
    kwargs = {}
    if embed_name:
        kwargs["model_name"] = embed_name
    if embed_key:
        kwargs["api_key"] = embed_key
    if embed_url:
        kwargs["base_url"] = embed_url
    
    print(f"配置参数: {list(kwargs.keys())}")
    dashscope_success = test_embedding("dashscope", **kwargs)
else:
    print("\n--- 跳过 DashScope（未配置）---")

# 4.2 测试本地模型
print("\n🟢 准备测试本地模型")
local_models = [
    "sentence-transformers/all-MiniLM-L6-v2",
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
]

local_success = False
for model_name in local_models:
    print(f"\n尝试模型: {model_name}")
    if test_embedding("local", model_name=model_name):
        local_success = True
        break

# 4.3 测试 TF-IDF
print("\n🟡 准备测试 TF-IDF 模型")
tfidf_success = False
try:
    from hello_agents.memory.embedding import TFIDFEmbedding
    tfidf_model = TFIDFEmbedding(max_features=100)
    # TF-IDF需要先训练
    corpus = ["这是第一个文档", "这是第二个文档", "第三个文档内容"]
    tfidf_model.fit(corpus)
    print("✅ TF-IDF 训练成功")
    
    test_vec = tfidf_model.encode("测试文本")
    print(f"✅ TF-IDF 编码成功，维度: {len(test_vec)}")
    tfidf_success = True
except Exception as e:
    print(f"❌ TF-IDF 失败: {e}")

# 5. 测试统一接口
print("\n【步骤5】测试统一接口")
unified_success = False
try:
    from hello_agents.memory.embedding import get_text_embedder, get_dimension
    
    print("正在获取全局嵌入器...")
    embedder = get_text_embedder()
    print(f"✅ 获取全局嵌入器成功")
    print(f"   类型: {type(embedder).__name__}")
    print(f"   维度: {get_dimension()}")
    
    test_result = embedder.encode("测试")
    print(f"✅ 编码测试成功，向量长度: {len(test_result)}")
    
    unified_success = True
except Exception as e:
    print(f"❌ 统一接口失败: {e}")

# 6. 总结
print("\n" + "="*60)
print("📊 诊断总结")
print("="*60)
print(f"DashScope模型: {'✅ 可用' if dashscope_success else '❌ 不可用'}")
print(f"本地模型:      {'✅ 可用' if local_success else '❌ 不可用'}")
print(f"TF-IDF模型:    {'✅ 可用' if tfidf_success else '❌ 不可用'}")
print(f"统一接口:      {'✅ 可用' if unified_success else '❌ 不可用'}")

# 7. 建议
print("\n💡 建议:")
if not unified_success:
    if dashscope_success:
        print("   ✅ 建议使用 DashScope 模型")
        print("   .env 配置:")
        print("   EMBED_MODEL_TYPE=dashscope")
        print(f"   EMBED_MODEL_NAME={embed_name or 'text-embedding-v3'}")
    elif local_success:
        print("   ✅ 建议使用本地模型")
        print("   .env 配置:")
        print("   EMBED_MODEL_TYPE=local")
        print("   EMBED_MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2")
    elif tfidf_success:
        print("   ⚠️  仅 TF-IDF 可用（性能较差）")
        print("   建议安装: pip install sentence-transformers")
    else:
        print("   ❌ 所有模型都不可用！")
        print("   请先安装包:")
        print(f"   cd {project_root}")
        print("   pip install -e .")
        
    if missing_packages:
        print(f"\n   缺失的包: {', '.join(missing_packages)}")
        print(f"   安装命令: pip install {' '.join(missing_packages)}")
else:
    print("   ✅ 系统正常，可以正常使用")

print("\n" + "="*60)
print("诊断完成！")
print("="*60)